import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    __table_args__ = {"sqlite_autoincrement": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )
