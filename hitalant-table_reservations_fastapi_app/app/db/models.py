from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Table(Base):
    __tablename__ = "tables"


class Reservation(Base):
    __tablename__ = "reservations"
