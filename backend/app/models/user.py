from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # # one user can sell many tickets
    # tickets: Mapped[list["Ticket"]] = relationship(back_populates="seller")