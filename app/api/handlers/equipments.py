from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database.database import get_session
from app.middlewares.equipments import EquipmentsMiddleware
from app.api.schemas.equipments import AddEquipmentSchema
from app.api.exceptions.exceptions import EquipmentAlreadyExistsException


router = APIRouter(
    prefix='/equipments',
    tags=['Equipments']
)

@router.get('/')
async def get_all_equipments(session: AsyncSession = Depends(get_session)):
    equipments_mw = EquipmentsMiddleware(session)
    equipments = await equipments_mw.find_all()
    return {'equipments': equipments}


@router.get('/{id}')
async def get_equipment_by_id(id: int, session: AsyncSession = Depends(get_session)):
    equipments_mw = EquipmentsMiddleware(session)
    equipment = await equipments_mw.find_one(id)
    return {'equipment': equipment}

@router.post('/')
async def add_equipment(equipment: AddEquipmentSchema, session: AsyncSession = Depends(get_session)):
    equipments_mw = EquipmentsMiddleware(session)
    try:
        equipment = await equipments_mw.add_one(equipment)
    except EquipmentAlreadyExistsException:
        return Response(
            status_code=EquipmentAlreadyExistsException.status_code,
            content=EquipmentAlreadyExistsException.detail,
        )
    return {'equipment': equipment}

@router.delete('/{id}')
async def delete_equipment(id: int, session: AsyncSession = Depends(get_session)):
    equipments_mw = EquipmentsMiddleware(session)
    await equipments_mw.delete_one_by_id(id)
    return {'response': f'deleted equipment by id={id} successfuly'}