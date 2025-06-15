from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database.database import get_session
from app.middlewares.orders import OrdersMiddleware
from app.api.schemas.orders import AddOrderSchema


router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.post('/')
async def add_order(order: AddOrderSchema, session: AsyncSession = Depends(get_session)):
    orders_mw = OrdersMiddleware(session)
    order = await orders_mw.add_one(order)
    return {'order': order}


@router.get('/')
async def get_all_orders(session: AsyncSession = Depends(get_session)):
    orders_mw = OrdersMiddleware(session)
    orders = await orders_mw.find_all()
    return {'orders': orders}

@router.get('/{id}')
async def get_order_by_id(id: int, session: AsyncSession = Depends(get_session)):
    orders_mw = OrdersMiddleware(session)
    order = await orders_mw.find_one_or_none_by_id(id)
    return {'order': order}

@router.delete('/{id}')
async def delete_order_by_id(id: int, session: AsyncSession = Depends(get_session)):
    orders_mw = OrdersMiddleware(session)
    await orders_mw.delete_one_by_id(id)
    return {'response': f'deleted order by id={id} successfuly'}
