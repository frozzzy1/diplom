from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AddEquipmentSchema(BaseModel):
    title: str
    description: str
    price_per_day: int
    quantity: int | None = 0


class ReadEquipmentSchema(BaseModel):
    id: int
    title: str
    description: str
    price_per_day: int
    quantity: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateEquipmentSchema(BaseModel):
    id: int
    title: str | None = None
    description: str | None = None
    price_per_day: int | None = None
    quantity: int | None = None
