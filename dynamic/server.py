from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
from ese774_frame.api_server import FastApiServer
from dummy_device.dummy_ctrl import DummyDeviceCtrl


class Config:
    HOST='127.0.0.1'
    PORT=int(os.environ.get('ESE774_DUMMY_PORT','8000'))

server=FastApiServer(device_cls=DummyDeviceCtrl, router_cls=None, config=Config, api_spec=None, object_name='dummy', dispatch_exclude={'dangerous_reset'}, device_kwargs={'initial_value':10}, lifespan_msg_prefix='DUMMY')
if __name__=='__main__':
    server.run(host=Config.HOST, port=Config.PORT)
