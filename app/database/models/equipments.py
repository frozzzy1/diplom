from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import BaseOrm


class EquipmentOrm(BaseOrm):
    __tablename__ = 'equipments'

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    price_per_day: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column(default=0)
