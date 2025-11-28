from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, DateTime, Integer, Boolean
from datetime import datetime
from .base import Base



class Escrow(Base):

    __tablename__ = "escrows"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)

    amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)

    is_released: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    released_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

