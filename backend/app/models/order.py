from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, DateTime, Enum
from datetime import datetime
from .base import Base
import enum

class OrderStatus(enum.Enum):
    PENDING_PAYMENT = "pending_payment"      
    PAID = "paid"                          
    TICKET_SENT = "ticket_sent"              
    WAITING_ENTRY_CONFIRMATION = "waiting_entry_confirmation"
    COMPLETED = "completed"                 
    REFUNDED = "refunded"                    

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    ticket_id: Mapped[int] = mapped_column(nullable=False)
    buyer_id: Mapped[int] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    got_in: Mapped[bool] = mapped_column(default=False)

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.PENDING_PAYMENT
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)