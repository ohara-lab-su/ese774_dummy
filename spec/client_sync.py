from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
PORT=int(os.environ.get('ESE774_DUMMY_PORT','8000'))
from dummy_device.sync_dummy_client import SyncDummyClient
from dummy_device.spec import DUMMY_API_SPEC
c=SyncDummyClient(server_ip='127.0.0.1',server_port=PORT,object_name='dummy',api_spec=DUMMY_API_SPEC)
try:
    assert c.ping()=='pong'; assert c.add(2,5)==7
    c.value=30; assert c.value==30
    assert c.status=='connected'
    c.scale=4.0; assert c.scale==4.0
    p=c.download_file('hello.txt','client_download_spec')
    assert Path(p).read_bytes()==b'hello from dummy device\n'
    print('SPEC_SYNC_OK')
finally: c.close()
