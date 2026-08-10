from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dummy_device.dummy_ctrl import DummyDeviceCtrl

d = DummyDeviceCtrl(initial_value=10)
assert d.ping() == 'pong'
assert d.add(2,5) == 7
assert d.value == 10
d.value = 20
assert d.value == 20
assert d.status == 'connected'
assert d.scale == 1.0
d.scale = 2.5
assert d.scale == 2.5
p = d.download_file('hello.txt', 'local_download')
assert Path(p).read_bytes() == b'hello from dummy device\n'
print('LOCAL_TEST_OK')
