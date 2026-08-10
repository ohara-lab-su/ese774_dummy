from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
PORT=int(os.environ.get('ESE774_DUMMY_PORT','8000'))
from dummy_device.sync_dummy_client import SyncDummyClient
c=SyncDummyClient(server_ip='127.0.0.1',server_port=PORT,object_name='dummy',api_spec=None)
try:
    assert c.ping()=='pong'; assert c.add(2,5)==7
    c.value=25; assert c.value==25
    assert c.router_name=='DummyRouterCtrl'
    p=c.download_file('hello.txt','client_download')
    assert Path(p).read_bytes()==b'hello from dummy device\n'
    print('DYNAMIC_ROUTER_SYNC_OK')
finally: c.close()
