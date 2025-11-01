from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from ..api.schemas.shipment import ShipmentCreate
from ..database.models import Shipment, ShipmentStatus


class ShipmentService:
    def __init__(self, session: AsyncSession):
        # Get database session to perform database operations
        self.session = session  # pyright: ignore[reportUnannotatedClassAttribute]

    # Get a shipment by id
    async def get(self, id: int) -> Shipment | None:
        return await self.session.get(Shipment, id)

    # Add a new shipment
    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),  # pyright: ignore[reportAny]
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    # Update an existing shipment
    async def update(self, id: int, shipment_update: dict) -> Shipment | None:  # pyright: ignore[reportUnknownParameterType]
        shipment = await self.get(id)
        shipment.sqlmodel_update(shipment_update)  # pyright: ignore[reportUnusedCallResult, reportUnknownArgumentType, reportOptionalMemberAccess]

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    # Delete a shipment
    async def delete(self, id: int) -> None:
        await self.session.delete(await self.get(id))
        await self.session.commit()
