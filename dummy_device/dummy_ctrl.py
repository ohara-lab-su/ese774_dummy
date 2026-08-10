from pathlib import Path

class DummyDeviceCtrl:
    """ese774_frame の手動統合試験用ダミーデバイス。"""
    def __init__(self, initial_value: int = 10, logger=None, log_level=None, **kwargs):
        self._value = int(initial_value)
        self._scale = 1.0
        self._logger = logger
        self._files = {
            "hello.txt": b"hello from dummy device\n",
            "data.bin": bytes(range(16)),
        }

    def disconnect(self):
        return None

    def ping(self) -> str:
        return "pong"

    def add(self, a: int, b: int) -> int:
        return a + b

    def mixed(self, a: int, b: float, text: str = "") -> float:
        return float(a) + float(b)

    def get_complex_result(self):
        return {"tuple": (1,2,3), "bytes": b"abc", "nested": {"value": self._value}}

    def dangerous_reset(self):
        self._value = 0
        return True

    def _private_api(self):
        return "private"

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = int(value)

    @property
    def status(self) -> str:
        return "connected"

    def get_scale(self) -> float:
        return self._scale

    def set_scale(self, value: float):
        self._scale = float(value)

    scale = property(get_scale, set_scale)

    def get_file_content(self, filename: str):
        if filename not in self._files:
            raise FileNotFoundError(filename)
        return {"filename": filename, "content": self._files[filename]}

    def download_file(self, filename: str, output_dir: str):
        """ローカル実行時はDeviceを実行しているPCへ保存する。"""
        data = self.get_file_content(filename)
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        path = out / filename
        path.write_bytes(data["content"])
        return str(path)
