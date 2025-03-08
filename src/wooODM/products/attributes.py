from pydantic import BaseModel
from typing import Optional
from wooODM.core import WooBasicODM

class ProductAttribute(WooBasicODM):
    """
    Represents a WooCommerce product attribute using Pydantic for validation & deserialization.
    """
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    name: str  # Attribute name (mandatory)
    slug: Optional[str] = None  # An alphanumeric identifier for the resource unique to its type
    type: str = "select"  # Type of attribute. By default only 'select' is supported
    order_by: str = "menu_order"  # Default sort order. Options: menu_order, name, name_num, and id. Default is 'menu_order'
    has_archives: bool = False  # Enable/Disable attribute archives. Default is False

    @classmethod
    def endpoint(cls, id: int = None) -> str:
        return "products/attributes" if id is None else f"products/attributes/{id}"

    def __repr__(self):
        return f"ProductAttribute(id={self.id}, name={self.name}, slug={self.slug}, type={self.type}, order_by={self.order_by}, has_archives={self.has_archives})"