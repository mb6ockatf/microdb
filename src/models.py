from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Payments(Base):
    __tablename__ = "payments"

    ID: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    subscription_until: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    ref_string: Mapped[str] = mapped_column(String(20), nullable=False)
