# ese774_dummy

`ese774_frame` の機能確認を目的としたダミーデバイスプロジェクトです。

実デバイスを使用したテストでは、そのデバイスが利用していない Framework 機能の確認が抜ける可能性があります。

本プロジェクトでは、Framework の主要機能を意図的に実装した共通の `DummyDeviceCtrl` を使用し、以下の動作を実デバイスに依存せず確認します。

- ローカル Device Class
- ApiSpec / Pydantic I/F モード
- 完全動的ディスパッチモード
- 完全動的ディスパッチ + Custom Router モード
- Sync / Async Client
- method のリモート呼び出し
- property の透過アクセス
- Custom Router による処理の override
- Client 側での処理の override
- private API / `dispatch_exclude`
- サーバーからクライアントへのファイル転送

`ese774_frame` はインストール済みであることを前提とします。

このプロジェクト自体を `pip install` する必要はありません。

---

## ディレクトリ構成

```text
ese774_dummy/
├── dummy_device/
│   ├── __init__.py
│   ├── dummy_ctrl.py
│   ├── dummy_router.py
│   ├── sync_dummy_client.py
│   ├── async_dummy_client.py
│   └── spec.py
│
├── local/
│   └── local_device_example.py
│
├── spec/
│   ├── server.py
│   └── client_sync.py
│
├── dynamic/
│   ├── server.py
│   ├── client_sync.py
│   └── client_async.py
│
└── dynamic_router/
    ├── server.py
    ├── client_sync.py
    ├── client_async.py
    └── client_smoke.py
```

`dummy_device/` は全モードで共通です。

`spec/`、`dynamic/`、`dynamic_router/` は、それぞれ異なる Framework の利用方法を確認するためのサーバー・クライアント実行環境です。

---

# テスト対象

## 通常 method

`DummyDeviceCtrl` には通常の method として、例えば以下を実装しています。

```python
device.ping()
device.add(a, b)
device.mixed(...)
device.get_complex_result()
```

ローカル呼び出し、および Framework 経由のリモート呼び出しを確認します。

---

## read/write property

通常の `@property` / setter を持つ property を確認します。

```python
@property
def value(self):
    ...

@value.setter
def value(self, value):
    ...
```

クライアント側でも、

```python
value = client.value
client.value = 123
```

として property のままアクセスできることを確認します。

---

## read-only property

setter を持たない property も確認します。

```python
@property
def status(self):
    ...
```

クライアント側では、

```python
status = client.status
```

としてアクセスします。

---

## `property()` による property

デコレータを使用せず、

```python
scale = property(get_scale, set_scale)
```

として定義した property も確認します。

クライアント側では、

```python
scale = client.scale
client.scale = 2.5
```

として利用します。

これにより、`@property` だけでなく Python 標準の `property()` で作成された静的 property も Framework が認識できることを確認します。

---

## private API

Device Class の、

```python
_private_api()
```

のような `_` で始まる member が、完全動的ディスパッチ時に公開 API として扱われないことを確認するためのものです。

---

## `dispatch_exclude`

Device Class にはテスト用として、

```python
dangerous_reset()
```

を実装しています。

サーバー起動時に、

```python
dispatch_exclude={"dangerous_reset"}
```

を指定し、完全動的モードであってもこの API が公開されないことを確認します。

`dynamic_router/client_smoke.py` では、`dangerous_reset()` へのアクセスが HTTP 404 になることを正常動作として確認します。

---

# local

Framework のHTTP通信を使用せず、`DummyDeviceCtrl` 自体の動作を確認します。

```bash
python local/local_device_example.py
```

主な確認項目：

- 通常 method
- read/write property
- read-only property
- `property()`
- ローカルファイル保存

Device Class 自体の基準動作を確認するためのモードです。

---

# ApiSpec / Pydantic I/F モード

`spec/` は従来の明示的な ApiSpec / Pydantic I/F を使用するモードです。

サーバーを起動します。

```bash
python spec/server.py
```

別ターミナルから Client を実行します。

```bash
python spec/client_sync.py
```

サーバーは概念的に以下の構成です。

```python
FastApiServer(
    device_cls=DummyDeviceCtrl,
    router_cls=DummyRouterCtrl,
    api_spec=DUMMY_API_SPEC,
    ...
)
```

主な確認項目：

- ApiSpec による明示的 API 定義
- Pydantic request / response model
- 従来 Router
- Sync Client
- 通常 method
- property getter / setter
- read-only property
- `property()`
- Router override
- Client override
- クライアント側ファイル保存

このモードは、従来の `ese774_frame` 利用方法との後方互換性確認にも使用します。

---

# 完全動的ディスパッチモード

`dynamic/` は、

```python
api_spec=None
router_cls=None
```

による完全動的ディスパッチを確認します。

サーバーを起動します。

```bash
python dynamic/server.py
```

同期 Client：

```bash
python dynamic/client_sync.py
```

非同期 Client：

```bash
python dynamic/client_async.py
```

サーバーは概念的に以下の構成です。

```python
FastApiServer(
    device_cls=DummyDeviceCtrl,
    router_cls=None,
    api_spec=None,
    ...
)
```

主な確認項目：

- ApiSpec なし
- 機器固有 Router なし
- Device Class からの API 自動検出
- method の動的 dispatch
- Sync Client
- Async Client
- read/write property
- read-only property
- `property()`
- private API の除外
- `dispatch_exclude`

このモードでは、機器側で ApiSpec や Router を記述しなくても、Device Class の通常 API を利用できることを確認します。

---

# 完全動的ディスパッチ + Custom Router

`dynamic_router/` は、

```python
api_spec=None
router_cls=DummyRouterCtrl
```

による動作を確認します。

サーバーを起動します。

```bash
python dynamic_router/server.py
```

同期 Client：

```bash
python dynamic_router/client_sync.py
```

非同期 Client：

```bash
python dynamic_router/client_async.py
```

サーバーは概念的に以下の構成です。

```python
FastApiServer(
    device_cls=DummyDeviceCtrl,
    router_cls=DummyRouterCtrl,
    api_spec=None,
    ...
)
```

通常 API は Framework の完全動的ディスパッチを使用し、一部の特殊な API だけを Custom Router で処理します。

主な確認項目：

- ApiSpec なし
- Device method の自動 dispatch
- Custom Router との共存
- Router method override
- Router property
- Client override
- Sync Client
- Async Client
- property
- `dispatch_exclude`
- クライアント側ファイル保存

---

# Router / Client override

`download_file()` は、サーバーとクライアントで処理内容が異なる API のテストに使用します。

ローカル Device では、

```text
Device
  ↓
Deviceを実行しているPCへ保存
```

となります。

リモート利用時には、

```text
Device
  ↓
DummyRouterCtrl
  ↓
ファイル内容をClientへ返す
  ↓
SyncDummyClient / AsyncDummyClient
  ↓
Client PCへ保存
```

となります。

API 名は同じ、

```python
download_file(...)
```

のまま、リモート利用時だけ Router / Client が処理を補います。

これは実デバイスにおける、

- ファイル取得
- 測定データ保存
- 画像取得

など、サーバーPCではなくクライアントPC側へ結果を保存する必要がある API を想定したテストです。

---

# Router property

`DummyRouterCtrl` には Router 側の property として、

```python
@property
def router_name(self):
    ...
```

を定義しています。

クライアント側から、

```python
client.router_name
```

としてアクセスできることを確認します。

これにより、完全動的ディスパッチと Custom Router を併用した場合に、Router 側の静的 property もクライアントへ反映されることを確認します。

---

# Smoke Test

`dynamic_router/client_smoke.py` は、完全動的ディスパッチ + Custom Router の主要機能をまとめて確認するためのスクリプトです。

最初にサーバーを起動します。

```bash
python dynamic_router/server.py
```

別ターミナルから実行します。

```bash
python dynamic_router/client_smoke.py
```

確認項目：

```text
[PASS] method ping
[PASS] method add
[PASS] property getter/setter
[PASS] read-only property getter
[PASS] property() getter/setter
[PASS] router property
[PASS] router override + client-side file save
[PASS] dispatch_exclude expected 404
```

すべて成功した場合：

```text
========================================
ALL TESTS PASSED
========================================
```

失敗した場合：

```text
[FAIL] ...
========================================
TEST FAILED
========================================
```

となります。

---

# テスト項目一覧

| 項目 | local | spec | dynamic | dynamic + router |
|---|:---:|:---:|:---:|:---:|
| 通常 method | ✓ | ✓ | ✓ | ✓ |
| ApiSpec / Pydantic | - | ✓ | - | - |
| 自動 dispatch | - | - | ✓ | ✓ |
| Sync Client | - | ✓ | ✓ | ✓ |
| Async Client | - | - | ✓ | ✓ |
| `@property` getter | ✓ | ✓ | ✓ | ✓ |
| `@property` setter | ✓ | ✓ | ✓ | ✓ |
| read-only property | ✓ | ✓ | ✓ | ✓ |
| `property()` | ✓ | ✓ | ✓ | ✓ |
| `_private` 除外 | - | - | ✓ | ✓ |
| `dispatch_exclude` | - | - | ✓ | ✓ |
| Custom Router | - | ✓ | - | ✓ |
| Router override | - | ✓ | - | ✓ |
| Router property | - | - | - | ✓ |
| Client override | - | ✓ | - | ✓ |
| Client側ファイル保存 | - | ✓ | - | ✓ |

---

# 推奨確認順序

Framework を変更した場合は、以下の順序で確認します。

```text
1. local
   ↓
2. spec
   ↓
3. dynamic
   ↓
4. dynamic_router
   ↓
5. dynamic_router/client_smoke.py
```

これにより、

```text
Device Class 自体の問題
        ↓
ApiSpec / Pydantic 後方互換性の問題
        ↓
完全動的 dispatch の問題
        ↓
Custom Router との協調動作の問題
        ↓
Client側処理の問題
```

と段階的に切り分けることができます。