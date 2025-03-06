from pydantic import BaseModel, Field
from typing import Optional
from wooODM.core import WooCommerce

class ProductTag(BaseModel):
    """
    Represents a WooCommerce product tag using Pydantic for validation & deserialization.
    """
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    name: str  # Tag name (mandatory)
    slug: Optional[str] = None  # Alphanumeric identifier unique to the tag
    description: Optional[str] = None  # HTML description of the tag
    count: Optional[int] = None  # Number of published products associated with the tag (read-only)
 
    def __repr__(self):
        return f"ProductTag(id={self.id}, name={self.name}, slug={self.slug}, product_count={self.count})"
    
    @classmethod
    def get(cls, tag_id: int):
        """
        Retrieve a product tag from WooCommerce by ID and return a ProductTag object.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(f"products/tags/{tag_id}")

        if response.status_code == 200:
            return cls.model_validate(response.json())
        
        raise Exception(response.json().get("message", "Unknown error"))
    
    def save(self):
        """
        Save the product tag to WooCommerce. Updates if it has an ID, otherwise creates a new one.
        """
        wcapi = WooCommerce.get_instance()
        data = self.dict(exclude_unset=True)  # Exclude unset fields

        # Create or update the product tag based on whether it has an ID
        if self.id:
            response = wcapi.put(f"products/tags/{self.id}", data)
        else:
            response = wcapi.post("products/tags", data)

        if response.status_code in [200, 201]:
            updated_tag = self.model_validate(response.json())
            for field, value in updated_tag.dict().items():
                setattr(self, field, value)
            return self

        raise Exception(response.json().get("message", "Unknown error"))

    def delete(self):
        """
        Delete the product tag from WooCommerce.
        """
        if not self.id:
            raise Exception("Tag has no ID. Cannot delete.")

        wcapi = WooCommerce.get_instance()
        response = wcapi.delete(f"products/tags/{self.id}")

        if response.status_code == 200:
            return response.json()  # Successfully deleted
        raise Exception(response.json().get("message", "Unknown error"))
