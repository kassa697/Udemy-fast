from enum import Enum
from pydantic import BaseModel, Field


# this class is used to define the status of a shipment
class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


# this class is used to define the base shipment model
class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int


class ShipmentRead(BaseShipment):
    status: ShipmentStatus


class Order(BaseModel):
    price: int
    title: str
    description: str


class ShipmentCreate(BaseShipment):
    order: Order


class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None, le=25)
    destination: int | None = Field(default=None)
    status: ShipmentStatus
