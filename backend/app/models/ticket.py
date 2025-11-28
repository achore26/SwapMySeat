from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, Enum
from .base import Base
import enum

class TicketStatus(enum.Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    TRANSFERRED = "transferred"
    VERIFIED_ENTRY = "verified_entry"
    CANCELLED = "cancelled"

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    event_id: Mapped[int] = mapped_column(nullable=False)
    seller_id: Mapped[int] = mapped_column(nullable=False)

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    seat_number: Mapped[str | None] = mapped_column(String(255))
    section: Mapped[str | None] = mapped_column(String(255))

    ticket_image_url: Mapped[str] = mapped_column(String(500), nullable=False)

    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus),
        nullable=False,
        default=TicketStatus.AVAILABLE
    )