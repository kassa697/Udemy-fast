# fastapi教材でやったこと

## pip install

```bash
# Macはダブルクォーテーション必要かも？
pip install "fastapi[all]"

# fastapi dev で動かなかった時にしたやつ
uvicorn main:app --reload

# 動画ではこれで動かした
fastapi dev

# scalar_fastapiはAPIドキュメント&SwaggerUIで使う
pip install scalar_fastapi

# sqlmodelはDBのORMで使う
pip install sqlmodel

# pydantic-settingsは環境変数から設定を読み込むためのライブラリ
pip install pydantic-settings

```

## メモ

パスの順番大事

OK例

```python
@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment/{id}")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if not id:
        id = max(shipments.keys())
        return shipments[id]
    if id not in shipments:
        return {"detail": "指定したIDは存在しません"}
    return shipments[id]
```

NG例
latestの前に動いてしまうかも
```python
@app.get("/shipment/{id}")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if not id:
        id = max(shipments.keys())
        return shipments[id]
    if id not in shipments:
        return {"detail": "指定したIDは存在しません"}
    return shipments[id]

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]
```
