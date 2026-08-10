from pathlib import Path
import logging
import sys

import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dummy_device.sync_dummy_client import SyncDummyClient


def run_check(name, func):
    try:
        func()
        print(f"[PASS] {name}")
        return True
    except Exception as exc:
        print(f"[FAIL] {name}: {type(exc).__name__}: {exc}")
        return False


def main() -> int:
    client = SyncDummyClient(
        server_ip="127.0.0.1",
        server_port=8000,
        object_name="dummy",
        api_spec=None,
    )

    results = []

    try:
        results.append(
            run_check(
                "method ping",
                lambda: None if client.ping() == "pong"
                else (_ for _ in ()).throw(AssertionError("ping != pong")),
            )
        )

        results.append(
            run_check(
                "method add",
                lambda: None if client.add(2, 5) == 7
                else (_ for _ in ()).throw(AssertionError("add(2, 5) != 7")),
            )
        )

        def check_value_property():
            client.value = 123
            assert client.value == 123

        results.append(
            run_check("property getter/setter", check_value_property)
        )

        results.append(
            run_check(
                "read-only property getter",
                lambda: None if client.status == "connected"
                else (_ for _ in ()).throw(
                    AssertionError("status != connected")
                ),
            )
        )

        def check_scale_property():
            client.scale = 2.5
            assert client.scale == 2.5

        results.append(
            run_check("property() getter/setter", check_scale_property)
        )

        results.append(
            run_check(
                "router property",
                lambda: None if client.router_name == "DummyRouterCtrl"
                else (_ for _ in ()).throw(
                    AssertionError(
                        f"router_name={client.router_name!r}"
                    )
                ),
            )
        )

        def check_router_download():
            path = client.download_file(
                "hello.txt",
                "client_smoke_download",
            )
            assert path.endswith("hello.txt")

        results.append(
            run_check(
                "router override + client-side file save",
                check_router_download,
            )
        )

        def check_excluded_api():
            client_log = logging.getLogger(
                "ese774_frame.clients.sync_device_client"
            )
            httpx_log = logging.getLogger("httpx")

            old_client_level = client_log.level
            old_httpx_level = httpx_log.level

            client_log.setLevel(logging.CRITICAL)
            httpx_log.setLevel(logging.CRITICAL)

            try:
                try:
                    client.dangerous_reset()
                except httpx.HTTPStatusError as exc:
                    assert exc.response.status_code == 404
                    return

                raise AssertionError(
                    "dangerous_reset was not rejected"
                )
            finally:
                client_log.setLevel(old_client_level)
                httpx_log.setLevel(old_httpx_level)

        results.append(
            run_check(
                "dispatch_exclude expected 404",
                check_excluded_api,
            )
        )

    finally:
        client.close()

    print("=" * 48)

    if all(results):
        print("ALL TESTS PASSED")
        print("=" * 48)
        return 0

    print("TEST FAILED")
    print("=" * 48)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
