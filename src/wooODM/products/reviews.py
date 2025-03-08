from pydantic import Field, EmailStr
from typing import Optional
from datetime import datetime
from wooODM.core import WooBasicODM

class ProductReview(WooBasicODM):
    """
    Represents a WooCommerce product review using Pydantic for validation & deserialization.
    """
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    date_created: Optional[datetime] = None  # The date the review was created (site's timezone, read-only)
    date_created_gmt: Optional[datetime] = None  # The date the review was created (GMT, read-only)
    product_id: int  # Unique identifier for the product that the review belongs to
    status: str = "approved"  # Status of the review (default is 'approved')
    reviewer: str  # Reviewer name
    reviewer_email: EmailStr  # Reviewer email
    review: str  # The content of the review
    rating: int = Field(..., ge=0, le=5)  # Review rating (0 to 5)
    verified: bool  # Shows if the reviewer bought the product or not

    @classmethod
    def endpoint(cls, id: int = None) -> str:
        return "products/reviews" if id is None else f"products/reviews/{id}"

    def __repr__(self):
        return f"ProductReview(id={self.id}, product_id={self.product_id}, reviewer={self.reviewer}, rating={self.rating}, verified={self.verified})"