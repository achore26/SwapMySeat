from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class TicketCreate(BaseModel):
    event_id: int
    price: Decimal
    seat_number: Optional[str] = None
    section: Optional[str] = None


class TicketResponse(BaseModel):
    id: int
    event_id: int
    price: Decimal
    seat_number: Optional[str]
    section: Optional[str]
    ticket_image_url: str
    status: str

    class Config:
        from_attributes = True