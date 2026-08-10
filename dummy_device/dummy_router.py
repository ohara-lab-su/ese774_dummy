from ese774_frame.routers.device_router import DeviceRouter

class DummyRouterCtrl(DeviceRouter):
    """サーバー/クライアントで意味が変わるAPIだけ override。"""
    def download_file(self, filename: str, output_dir: str):
        data = self._device.get_file_content(filename)
        return {"filename": data["filename"], "content": data["content"], "output_dir": output_dir}

    @property
    def router_name(self) -> str:
        return self.__class__.__name__
