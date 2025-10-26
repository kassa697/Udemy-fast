from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from .database import save, shipments

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


app = FastAPI()

### Shipments datastore as dict


###  a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int) -> ShipmentRead:
    # Check for shipment with given id
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )
    return shipments[id]


### Create a new shipment with conptent and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    # Create and assign shipment a new id
    new_id = max(shipments.keys()) + 1
    # Add to shipments dict
    shipments[new_id] = {
        **shipment.model_dump(),  # this line is used to copy all attributes from the shipment object to the new shipment dictionary
        "id": new_id,
        "status": "placed",
    }
    save()
    # Return id for later use
    return {"id": new_id}


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):
    # Update data with given fields
    shipments[id].update(body.model_dump(exclude_none=True))
    save()
    return shipments[id]


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    # Remove from datastore
    shipments.pop(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
