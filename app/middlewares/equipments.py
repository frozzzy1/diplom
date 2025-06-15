from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.exceptions.exceptions import EquipmentAlreadyExistsException
from app.api.schemas.equipments import AddEquipmentSchema, ReadEquipmentSchema
from app.api.schemas.users import ReadUserSchema
from app.database.repositories.equipments import EquipmentsRepository


class EquipmentsMiddleware:

    def __init__(self, session: AsyncSession):
        self.equip_repository = EquipmentsRepository(session)

    async def find_all(self) -> list[ReadUserSchema]:
        equipments = await self.equip_repository.find_all()
        return equipments
    
    async def find_one(self, id: int) -> ReadEquipmentSchema:
        equipment = await self.equip_repository.find_one(id)
        return equipment
    
    async def add_one(self, e: AddEquipmentSchema) -> ReadEquipmentSchema:
        try:
            equipment = await self.equip_repository.add_one(e)
        except IntegrityError:
            raise EquipmentAlreadyExistsException
        return equipment
    
    async def delete_one_by_id(self, id: int) -> None:
        await self.equip_repository.delete_one_by_id(id)
