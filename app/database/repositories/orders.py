from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.schemas.orders import AddOrderSchema, ReadOrderSchema
from app.database.models.equipments import EquipmentOrm
from app.database.models.orders import OrderOrm
from app.database.models.users import UserOrm
from app.utils.repo import AbsRepo


class OrdersRepository(AbsRepo):
    
    async def add_one(self, data: AddOrderSchema) -> ReadOrderSchema:
        order = OrderOrm(**data.model_dump())
        equip_sql = select(EquipmentOrm).filter(EquipmentOrm.id == order.equipment_id)
        equipment = await self.session.scalar(equip_sql)
        order.final_price = ((order.end_date - order.start_date).days + 1) * equipment.price_per_day
        try:
            self.session.add(order)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(order)
        return ReadOrderSchema.model_validate(order)
    
    async def find_all(self) -> list[ReadOrderSchema]:
        query = select(OrderOrm)
        result = await self.session.scalars(query)
        return [ReadOrderSchema.model_validate(i).model_dump() for i in result]
    
    async def find_one_or_none_by_id(self, id: int) -> ReadOrderSchema | None:
        query = select(OrderOrm).filter(OrderOrm.id == id)
        result = await self.session.scalar(query)
        if result:
            return ReadOrderSchema.model_validate(result)
        return

    async def delete_one_by_id(self, id: int) -> None:
        query = delete(OrderOrm).filter(OrderOrm.id == id)
        await self.session.execute(query)
        await self.session.commit()
