from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
PORT=int(os.environ.get('ESE774_DUMMY_PORT','8000'))
from ese774_frame.clients.sync_device_client import SyncDeviceClient
c=SyncDeviceClient(server_ip='127.0.0.1',server_port=PORT,object_name='dummy',api_spec=None)
try:
    assert c.ping()=='pong'
    assert c.add(2,5)==7
    assert c.mixed(1,1.5,'x')==2.5
    z=c.get_complex_result(); assert z['tuple']==(1,2,3) and z['bytes']==b'abc'
    c.value=25; assert c.value==25
    assert c.status=='connected'
    c.scale=3.0; assert c.scale==3.0
    print('DYNAMIC_SYNC_OK')
finally: c.close()
