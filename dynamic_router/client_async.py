from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
PORT=int(os.environ.get('ESE774_DUMMY_PORT','8000'))
import asyncio
from dummy_device.async_dummy_client import AsyncDummyClient
async def main():
    c=AsyncDummyClient(server_ip='127.0.0.1',server_port=PORT,object_name='dummy',api_spec=None)
    try:
        assert await c.ping()=='pong'; assert await c.add(2,5)==7
        c.value=40; assert c.value==40
        assert c.router_name=='DummyRouterCtrl'
        p=await c.download_file('data.bin','client_download_async')
        assert Path(p).read_bytes()==bytes(range(16))
        print('DYNAMIC_ROUTER_ASYNC_OK')
    finally: await c.close()
if __name__=='__main__': asyncio.run(main())
