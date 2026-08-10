from pathlib import Path
from ese774_frame.clients.async_device_client import AsyncDeviceClient

class AsyncDummyClient(AsyncDeviceClient):
    """remote semantics が異なるAPIだけ client側処理を override。"""
    async def download_file(self, filename: str, output_dir: str):
        if self.__dict__.get("_auto_dispatch", False):
            result = await self.dispatch("download_file", filename, output_dir)
        else:
            raw = getattr(self, "_download_file_raw")
            result = await raw(filename, output_dir)
        path = Path(output_dir) / result["filename"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(result["content"])
        return str(path)
