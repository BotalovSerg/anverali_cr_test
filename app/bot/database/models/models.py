from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    time_create: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
