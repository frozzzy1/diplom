from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class AddOrderSchema(BaseModel):
    user_id: int
    equipment_id: int
    start_date: date
    end_date: date


class ReadOrderSchema(BaseModel):
    id: int
    user_id: int
    equipment_id: int
    start_date: date
    end_date: date
    final_price: int
    order_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateOrderSchema(BaseModel):
    id: int
    start_date: date | None = None
    end_date: date | None = None
    order_type: str | None = None
