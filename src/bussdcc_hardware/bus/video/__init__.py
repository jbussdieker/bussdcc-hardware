from typing import Iterable, Dict

from cv2_enumerate_cameras import enumerate_cameras

from bussdcc.device import Device


class VideoBus(Device):
    kind = "bus"

    def discover(self) -> Iterable[str]:
        """
        Return camera indices as string device IDs.
        """
        return [str(camera_info.index) for camera_info in enumerate_cameras()]

    def get_metadata(self) -> Dict[str, Dict[str, int | str | None]]:
        """
        Optional: richer structured information.
        """
        return {
            str(info.index): {
                "index": info.index,
                "name": info.name,
                "path": info.path,
                "vid": info.vid,
                "pid": info.pid,
                "backend": info.backend,
            }
            for info in enumerate_cameras()
        }
