from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class Product(Base):
    __tablename__ = "products"

    article: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    price_sale: Mapped[float] = mapped_column(nullable=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    total_quantity: Mapped[int] = mapped_column(nullable=False)
