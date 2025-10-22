from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    123: {
        "weight": 10.2,
        "content": "wooden table",
        "status": "in transit",
    },
    456: {
        "weight": 5.5,
        "content": "metal chair",
        "status": "delivered",
    },
    789: {
        "weight": 2.3,
        "content": "plastic cup",
        "status": "pending",
    },
    101: {
        "weight": 3.1,
        "content": "glass vase",
        "status": "cancelled",
    },
    202: {
        "weight": 15.6,
        "content": "leather sofa",
        "status": "in transit",
    },
    303: {
        "weight": 1.2,
        "content": "ceramic bowl",
        "status": "delivered",
    },
}


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="指定したIDは存在しません"
        )
    return shipments[id]


@app.post("/shipment")
def submit_shipment(weight: float, data: dict[str, Any]) -> dict[str, int]:
    content = data["content"]

    if data["weight"] > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="重量が上限を超えています",
        )
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed",
    }

    return {"id": new_id}


# scalar fastapi document
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar FastAPI")


# # memo: パスの順番は重量。もし{id}を先に指定するとlatestが読まれない。
# @app.get("/shipment/latest")
# def get_latest_shipment() -> dict[str, Any]:
#     id = max(shipments.keys())
#     return shipments[id]
