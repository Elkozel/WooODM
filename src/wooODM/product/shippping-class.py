from pydantic import BaseModel
from typing import Optional
from wooODM.core import WooBasicODM

class ShippingClass(WooBasicODM):
    """
    Represents a WooCommerce product shipping class using Pydantic for validation & deserialization.
    """
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    name: str  # Shipping class name (mandatory)
    slug: Optional[str] = None  # An alphanumeric identifier for the resource unique to its type
    description: Optional[str] = None  # HTML description of the resource
    count: Optional[int] = None  # Number of published products for the resource (read-only)

    @classmethod
    def endpoint(cls, id: int = None) -> str:
        return "products/shipping_classes" if id is None else f"products/shipping_classes/{id}"

    def __repr__(self):
        return f"ShippingClass(id={self.id}, name={self.name}, slug={self.slug}, count={self.count})"