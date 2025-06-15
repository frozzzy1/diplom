from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import BaseOrm


class OrderOrm(BaseOrm):
    __tablename__ = 'orders'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    equipment_id: Mapped[int] = mapped_column(ForeignKey('equipments.id'))
    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()
    final_price: Mapped[int] = mapped_column()
    order_type: Mapped[str] = mapped_column(default='in_cart')
