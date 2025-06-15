from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.schemas.equipments import AddEquipmentSchema, ReadEquipmentSchema
from app.database.models.equipments import EquipmentOrm
from app.utils.repo import AbsRepo


class EquipmentsRepository(AbsRepo):
    async def find_all(self) -> list[ReadEquipmentSchema]:
        query = select(EquipmentOrm)
        result = await self.session.scalars(query)
        return [ReadEquipmentSchema.model_validate(i).model_dump() for i in result]
    
    async def find_one(self, id: int) -> ReadEquipmentSchema:
        query = select(EquipmentOrm).filter(EquipmentOrm.id == id)
        result = await self.session.scalar(query)
        return ReadEquipmentSchema.model_validate(result).model_dump()
    
    async def add_one(self, data: AddEquipmentSchema) -> ReadEquipmentSchema:
        equipment = EquipmentOrm(**data.model_dump())
        try:
            self.session.add(equipment)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(equipment)
        return ReadEquipmentSchema.model_validate(equipment)
    
    async def delete_one_by_id(self, id: int) -> None:
        query = delete(EquipmentOrm).filter(EquipmentOrm.id == id)
        await self.session.execute(query)
        await self.session.commit()

