from typing import Any, Optional
import threading

import cv2

from bussdcc.device import Device


class USBCamera(Device):
    kind = "camera"

    MAX_CONSECUTIVE_FAILURES = 3

    def __init__(self, *, id: str, config: dict[str, Any]):
        super().__init__(id=id, config=config)
        self._lock = threading.Lock()
        self._consecutive_failures = 0
        self.cap: cv2.VideoCapture | None = None
        self.desired_config = (config or {}).copy()
        self.device_index = int(self.config.get("device_index", 0))

    def _str_to_fourcc(self, val: str) -> int:
        if val == "AUTO":
            return 0

        if len(val) != 4:
            raise ValueError("FOURCC must be exactly 4 characters")

        return (
            ord(val[0]) | (ord(val[1]) << 8) | (ord(val[2]) << 16) | (ord(val[3]) << 24)
        )

    def _fourcc_to_str(self, val: float) -> str:
        if val == 0:
            return "AUTO"

        h = int(val)
        return (
            chr(h & 0xFF)
            + chr((h >> 8) & 0xFF)
            + chr((h >> 16) & 0xFF)
            + chr((h >> 24) & 0xFF)
        )

    def _get_exposure(self) -> Any:
        if self.cap is None:
            return

        backend = self.get_backend_name()
        if backend == "V4L2":  # Linux
            return self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE) == 3.0
        elif backend == "AVFOUNDATION":  # macOS
            return self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE) == 0.0
        else:
            return self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE) == 3.0

    def _apply_config(self) -> None:
        if self.cap is None:
            return

        cfg = self.desired_config
        backend = self.get_backend_name()

        fmt = self._str_to_fourcc(cfg["format"])
        self.cap.set(cv2.CAP_PROP_FOURCC, fmt)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg["width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg["height"])
        self.cap.set(cv2.CAP_PROP_FPS, cfg["fps"])
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        auto_focus = cfg.get("auto_focus", True)
        if auto_focus:
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1.0)
        else:
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0.0)
            self.cap.set(cv2.CAP_PROP_FOCUS, cfg["focus"])

        auto_wb = cfg.get("auto_white_balance", True)
        if auto_wb:
            self.cap.set(cv2.CAP_PROP_AUTO_WB, 1.0)
        else:
            self.cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
            self.cap.set(cv2.CAP_PROP_WB_TEMPERATURE, cfg["white_balance_temperature"])

        # Exposure control
        auto_exposure = cfg.get("auto_exposure", True)
        if backend == "V4L2":  # Linux
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3.0 if auto_exposure else 1.0)
            if not auto_exposure and "exposure" in cfg:
                self.cap.set(cv2.CAP_PROP_EXPOSURE, cfg["exposure"])
                self.cap.set(cv2.CAP_PROP_GAIN, cfg["gain"])
        elif backend == "AVFOUNDATION":  # macOS
            # AVFoundation sometimes ignores auto_exposure, so set exposure manually
            if not auto_exposure and "exposure" in cfg:
                self.cap.set(cv2.CAP_PROP_EXPOSURE, cfg["exposure"])
                self.cap.set(cv2.CAP_PROP_GAIN, cfg["gain"])
        else:
            # Fallback for unknown backends
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3.0 if auto_exposure else 1.0)
            if not auto_exposure and "exposure" in cfg:
                self.cap.set(cv2.CAP_PROP_EXPOSURE, cfg["exposure"])
                self.cap.set(cv2.CAP_PROP_GAIN, cfg["gain"])

    def _maybe_recover(self) -> None:
        if self._consecutive_failures >= self.MAX_CONSECUTIVE_FAILURES:
            self._consecutive_failures = 0
            self._reset_camera()

    def _reset_camera(self) -> None:
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
        self.cap = None

        self.connect()

    def get_backend_name(self) -> str | None:
        if not self.cap or not self.cap.isOpened():
            return None
        return self.cap.getBackendName() or "UNKNOWN"

    def get_config(self) -> dict[str, Any] | None:
        if not self.cap or not self.cap.isOpened():
            return None

        return {
            "desired": self.desired_config.copy(),
            "reported": {
                "format": self._fourcc_to_str(self.cap.get(cv2.CAP_PROP_FOURCC)),
                "width": self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                "height": self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
                "fps": self.cap.get(cv2.CAP_PROP_FPS),
                "auto_exposure": self._get_exposure(),
                "exposure": self.cap.get(cv2.CAP_PROP_EXPOSURE),
                "gain": self.cap.get(cv2.CAP_PROP_GAIN),
                "auto_white_balance": self.cap.get(cv2.CAP_PROP_AUTO_WB) == 1.0,
                "white_balance_temperature": self.cap.get(cv2.CAP_PROP_WB_TEMPERATURE),
                "auto_focus": self.cap.get(cv2.CAP_PROP_AUTOFOCUS) == 1.0,
                "focus": self.cap.get(cv2.CAP_PROP_FOCUS),
            },
        }

    def update_config(self, new_config: dict[str, Any]) -> None:
        with self._lock:
            self.desired_config.update(new_config)
            if self.cap and self.cap.isOpened():
                if "format" in new_config:
                    self.cap.release()
                    self.connect()
                else:
                    self._apply_config()

    def connect(self) -> None:
        self.cap = cv2.VideoCapture(self.device_index)
        if not self.cap.isOpened():
            raise RuntimeError("Camera not available")

        self._apply_config()

    def disconnect(self) -> None:
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.cap = None

    def read(self) -> tuple[bool, Any | None, dict[str, Any]]:
        with self._lock:
            if not self.cap or not self.cap.isOpened():
                self._consecutive_failures += 1
                self._maybe_recover()
                return False, None, {}

            ret, frame = self.cap.read()

        if not ret:
            self._consecutive_failures += 1
            self._maybe_recover()
            return False, None, {}

        # success path
        self._consecutive_failures = 0

        flip_v = self.desired_config.get("flip_vertical", False)
        flip_h = self.desired_config.get("flip_horizontal", False)
        if flip_v and flip_h:
            frame = cv2.flip(frame, -1)  # both axes
        elif flip_v:
            frame = cv2.flip(frame, 0)  # vertical
        elif flip_h:
            frame = cv2.flip(frame, 1)  # horizontal

        config = self.get_config() or {}
        metadata = {
            "time": self.ctx.clock.now_utc().isoformat() if self.ctx else None,
            "backend": self.get_backend_name(),
            **config,
        }

        return ret, frame, metadata
