from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    SmallInteger,
    String,
    text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Table(Base):
    __tablename__ = 'tables'

    table_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    seats: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    location: Mapped[str] = mapped_column(String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'name', 'seats', 'location',
            name='table_unique'
        ),
    )


class Reservation(Base):
    __tablename__ = 'reservations'

    reservation_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(32), nullable=False)
    reservation_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now(), server_default=text('CURRENT_TIMESTAMP'))
    duration_minutes: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    table_id: Mapped[int] = mapped_column(ForeignKey('tables.table_id', ondelete='CASCADE'), nullable=False)
    table: Mapped['Table'] = relationship()

    __table_args__ = (
        UniqueConstraint(
            'table_id', 'reservation_time',
            name='table_time_unique'
        ),
    )
