from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
PORT=int(os.environ.get('ESE774_DUMMY_PORT','8000'))
import asyncio
from ese774_frame.clients.async_device_client import AsyncDeviceClient
async def main():
    c=AsyncDeviceClient(server_ip='127.0.0.1',server_port=PORT,object_name='dummy',api_spec=None)
    try:
        assert await c.ping()=='pong'
        assert await c.add(2,5)==7
        c.value=40; assert c.value==40
        assert c.status=='connected'
        c.scale=5.0; assert c.scale==5.0
        print('DYNAMIC_ASYNC_OK')
    finally: await c.close()
if __name__=='__main__': asyncio.run(main())
