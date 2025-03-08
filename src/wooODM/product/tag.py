from pydantic import BaseModel, Field
from typing import Optional
from wooODM.core import WooBasicODM, WooCommerce

class ProductTag(WooBasicODM):
    """
    Represents a WooCommerce product tag using Pydantic for validation & deserialization.
    """
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    name: str  # Tag name (mandatory)
    slug: Optional[str] = None  # Alphanumeric identifier unique to the tag
    description: Optional[str] = None  # HTML description of the tag
    count: Optional[int] = None  # Number of published products associated with the tag (read-only)

    @classmethod
    def endpoint(cls, id: int = None) -> str:
        return "products/tags" if id is None else f"products/tags/{id}"
 
    def __repr__(self):
        return f"ProductTag(id={self.id}, name={self.name}, slug={self.slug}, product_count={self.count})"