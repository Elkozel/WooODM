from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Image(BaseModel):
    """
    Represents an image resource in WooCommerce.
    """
    id: Optional[int] = None  # Unique image ID (read-only)
    date_created: Optional[datetime] = None  # Date created (site timezone, read-only)
    date_created_gmt: Optional[datetime] = None  # Date created (GMT, read-only)
    date_modified: Optional[datetime] = None  # Date modified (site timezone, read-only)
    date_modified_gmt: Optional[datetime] = None  # Date modified (GMT, read-only)
    src: str  # Image URL
    name: Optional[str] = None  # Image name
    alt: Optional[str] = None  # Image alternative text

    def __repr__(self):
        return f"Image(id={self.id}, src='{self.src}', name='{self.name}', alt='{self.alt}')"
