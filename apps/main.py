from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from .database import Database

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


app = FastAPI()

db = Database()


@app.on_event("startup")
def startup_db_client():
    db.connect_to_db()
    db.create_table()


@app.on_event("shutdown")
def shutdown_db_client():
    db.close()


### Shipments datastore as dict


###  a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int) -> ShipmentRead:
    # Check for shipment with given id
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )
    return shipment


### Create a new shipment with conptent and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.create(shipment)
    # Return id for later use
    return {"id": new_id}


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):
    # Update data with given fields
    shipment = db.update(id, body)
    return shipment


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    # Remove from datastore
    db.delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
