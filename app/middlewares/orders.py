from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.schemas.orders import AddOrderSchema, ReadOrderSchema
from app.api.schemas.orders import ReadOrderSchema
from app.database.repositories.orders import OrdersRepository


class OrdersMiddleware:

    def __init__(self, session: AsyncSession):
        self.order_repository = OrdersRepository(session)
    
    async def add_one(self, o: AddOrderSchema) -> ReadOrderSchema:
        return await self.order_repository.add_one(o)
    
    async def find_all(self) -> list[ReadOrderSchema]:
        return await self.order_repository.find_all()
    
    async def find_one_or_none_by_id(self, id: int) -> ReadOrderSchema | None:
        return await self.order_repository.find_one_or_none_by_id(id)
    
    async def delete_one_by_id(self, id: int) -> None:
        await self.order_repository.delete_one_by_id(id)
