from pydantic import BaseModel
from ese774_frame.models.api_spec import ApiSpec

class AddRequest(BaseModel):
    a: int
    b: int
class AddResponse(BaseModel):
    result: int
class PingResponse(BaseModel):
    result: str
class DownloadRequest(BaseModel):
    filename: str
    output_dir: str
class DownloadResponse(BaseModel):
    filename: str
    content: bytes
    output_dir: str

DUMMY_API_SPEC = [
    ApiSpec(request_model=None, response_model=PingResponse, name='ping', object_name='dummy', method='post'),
    ApiSpec(request_model=AddRequest, response_model=AddResponse, name='add', object_name='dummy', method='post'),
    ApiSpec(request_model=None, response_model=None, name='value', object_name='dummy', method='get', kind='property', writable=True),
    ApiSpec(request_model=None, response_model=None, name='status', object_name='dummy', method='get', kind='property', writable=False),
    ApiSpec(request_model=None, response_model=None, name='scale', object_name='dummy', method='get', kind='property', writable=True),
    ApiSpec(request_model=DownloadRequest, response_model=DownloadResponse, name='download_file', object_name='dummy', method='post'),
]
