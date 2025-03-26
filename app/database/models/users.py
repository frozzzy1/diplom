from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import BaseOrm


class UserOrm(BaseOrm):
    __tablename__ = 'users'

    full_name: Mapped[str] = mapped_column()
    login: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(default='user')
