from typing import Optional
from datetime import datetime
from wooODM.core import WooDoubleIdODM

class OrderNote(WooDoubleIdODM):
    """
    Represents a WooCommerce order note using Pydantic for validation & deserialization.
    """
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    author: Optional[str] = None  # Order note author (read-only)
    date_created: Optional[datetime] = None  # The date the order note was created (site's timezone) (read-only)
    date_created_gmt: Optional[datetime] = None  # The date the order note was created (GMT) (read-only)
    note: str  # Order note content (mandatory)
    customer_note: bool = False  # If true, the note will be shown to customers and they will be notified. Default is false.
    added_by_user: bool = False  # If true, this note will be attributed to the current user. Default is false.

    @classmethod
    def endpoint(cls, id1: int, id2: int = None) -> str:
        assert id is not None, "Variation ID is mandatory"
        return f"orders/{id1}/notes/{id2}" if id2 else f"orders/{id1}/notes/"

    def __repr__(self):
        return f"OrderNote(id={self.id}, author={self.author}, note={self.note}, customer_note={self.customer_note})"