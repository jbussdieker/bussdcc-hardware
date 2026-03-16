from typing import Any, Optional
import threading

import cv2

from bussdcc import Device

from .config import USBCameraConfig


class USBCamera(Device[USBCameraConfig]):
    kind = "camera"

    MAX_CONSECUTIVE_FAILURES = 3

    def __init__(self, *, id: str, config: USBCameraConfig):
        super().__init__(id=id, config=config)
        self._lock = threading.Lock()
        self._consecutive_failures = 0
        self.cap: cv2.VideoCapture | None = None

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

        backend = self.get_backend_name()

        fmt = self._str_to_fourcc(self.config.format)
        self.cap.set(cv2.CAP_PROP_FOURCC, fmt)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.config.fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, self.config.buffersize)

        if self.config.auto_focus:
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1.0)
        else:
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0.0)
            self.cap.set(cv2.CAP_PROP_FOCUS, self.config.focus)

        if self.config.auto_white_balance:
            self.cap.set(cv2.CAP_PROP_AUTO_WB, 1.0)
        else:
            self.cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
            self.cap.set(
                cv2.CAP_PROP_WB_TEMPERATURE, self.config.white_balance_temperature
            )

        # Exposure control
        if backend == "V4L2":  # Linux
            self.cap.set(
                cv2.CAP_PROP_AUTO_EXPOSURE, 3.0 if self.config.auto_exposure else 1.0
            )
            if not self.config.auto_exposure:
                self.cap.set(cv2.CAP_PROP_EXPOSURE, self.config.exposure)
                self.cap.set(cv2.CAP_PROP_GAIN, self.config.gain)
        elif backend == "AVFOUNDATION":  # macOS
            # AVFoundation sometimes ignores auto_exposure, so set exposure manually
            if not self.config.auto_exposure:
                self.cap.set(cv2.CAP_PROP_EXPOSURE, self.config.exposure)
                self.cap.set(cv2.CAP_PROP_GAIN, self.config.gain)
        else:
            # Fallback for unknown backends
            self.cap.set(
                cv2.CAP_PROP_AUTO_EXPOSURE, 3.0 if self.config.auto_exposure else 1.0
            )
            if not self.config.auto_exposure:
                self.cap.set(cv2.CAP_PROP_EXPOSURE, self.config.exposure)
                self.cap.set(cv2.CAP_PROP_GAIN, self.config.gain)

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

    def update_config(self, new_config: USBCameraConfig) -> None:
        with self._lock:
            reconnect = False
            if self.config.format != new_config.format:
                reconnect = True

            self._config = new_config
            if self.cap and self.cap.isOpened():
                if reconnect:
                    self.cap.release()
                    self.connect()
                else:
                    self._apply_config()

    def connect(self) -> None:
        self.cap = cv2.VideoCapture(self.config.device_index)
        if not self.cap.isOpened():
            raise RuntimeError("Camera not available")

        self._apply_config()

    def disconnect(self) -> None:
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.cap = None

    def read(self) -> tuple[bool, Any | None, dict[str, Any] | None]:
        with self._lock:
            if self.cap is None or not self.cap.isOpened():
                self._consecutive_failures += 1
                self._maybe_recover()
                return False, None, None

            # flush stale frames to reduce latency
            for _ in range(self.config.flush_frames):
                self.cap.grab()

            # grab new frame
            if not self.cap.grab():
                self._consecutive_failures += 1
                self._maybe_recover()
                return False, None, None

            # timestamp immediately after grabbing
            t = self.ctx.clock.now_utc() if self.ctx else None

            # retrieve the frame
            ok, frame = self.cap.retrieve()
            if not ok:
                self._consecutive_failures += 1
                self._maybe_recover()
                return False, None, None

            # success, reset failure count
            self._consecutive_failures = 0
            self.set_online()

            metadata = {
                "time": t.isoformat() if t else None,
                "device": self.id,
            }

            return True, frame, metadata
