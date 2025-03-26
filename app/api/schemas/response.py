from pydantic import BaseModel


class ResponseSchema(BaseModel):
    data: dict | None = None
