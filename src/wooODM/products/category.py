from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

from wooODM.core import WooBasicODM
class ImageProperties(BaseModel):
    """
    Represents the image properties for a WooCommerce product category.
    """
    id: Optional[int] = None  # Image ID
    date_created: Optional[datetime] = None  # The date the image was created (site's timezone, read-only)
    date_created_gmt: Optional[datetime] = None  # The date the image was created (GMT, read-only)
    date_modified: Optional[datetime] = None  # The date the image was last modified (site's timezone, read-only)
    date_modified_gmt: Optional[datetime] = None  # The date the image was last modified (GMT, read-only)
    src: Optional[str] = None  # Image URL
    name: Optional[str] = None  # Image name
    alt: Optional[str] = None  # Image alternative text

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
    image: Optional[ImageProperties] = None  # Image data, see Product category - Image properties
    menu_order: int = 0  # Menu order for custom sorting the category
    count: Optional[int] = 0  # Number of published products in the category (read-only)

    @classmethod
    def endpoint(cls, id: int = None) -> str:
        return "products/categories" if id is None else f"products/categories/{id}"
    
    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, slug={self.slug}, product_count={self.count})"
