from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class BaseOrm(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.now())
