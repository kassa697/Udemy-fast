from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import Session, SQLModel

from app.config import settings

# Create a database engine to connect with database
engine = create_async_engine(
    # database type/dialect and file name
    url=settings.POSTGRES_URL,
    # Log sql queries
    echo=True,
)


async def create_db_tables():
    async with engine.begin() as connection:
        from .models import Shipment  # noqa: F401

        await connection.run_sync(SQLModel.metadata.create_all)


# Session to interact with database
async def get_session():
    async with AsyncSession(bind=engine) as session:
        yield session


# Session Dependency Annotation
SessionDep = Annotated[Session, Depends(get_session)]
