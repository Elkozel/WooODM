from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from wooODM.core import WooBasicODM, WooCommerce

class Category(WooBasicODM):
    """
    Represents a WooCommerce product category using Pydantic for validation & deserialization.
    """
    id: Optional[int] = None  # Unique identifier for the category (read-only)
    name: str  # Category name (mandatory)
    slug: str  # Alphanumeric identifier for the category
    parent: Optional[int] = 0  # Parent ID of the category, 0 means no parent (optional)
    description: Optional[str] = None  # HTML description of the category (optional)
    display: str = "default"  # Category archive display type, default is 'default'
    image: Optional[Dict[str, Any]] = None  # Image data, see Product category - Image properties
    menu_order: int = 0  # Menu order for custom sorting the category
    count: Optional[int] = 0  # Number of published products in the category (read-only)

    @classmethod
    def endpoint(cls) -> str:
        return "products/categories"
    
    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, slug={self.slug}, product_count={self.count})"
