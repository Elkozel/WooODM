from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from wooODM.core import WooCommerce

class Category(BaseModel):
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
    def get(cls, category_id: int):
        """
        Retrieve a category from WooCommerce by ID and return a Category object.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(f"products/categories/{category_id}")
        if response.status_code == 200:
            return cls.model_validate(response.json())
        raise Exception(response.json().get("message", "Unknown error"))

    @classmethod
    def get_by_slug(cls, slug: str):
        """
        Retrieve a category from WooCommerce by slug and return a Category object.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(f"products/categories?slug={slug}")
        categories = response.json()
        if categories:
            return cls.model_validate(categories[0])
        raise Exception("No category found for slug " + slug)

    @classmethod
    def all(cls, per_page: int = 10, page: int = 1):
        """
        Fetch all categories with pagination and return a list of Category objects.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(f"products/categories")

        if response.status_code == 200:
            return [cls.model_validate(product) for product in response.json()]
        
        raise Exception(response.json().get("message", "Unknown error"))

    def save(self):
        """
        Save the category to WooCommerce. Updates if it has an ID, otherwise creates a new one.
        """
        wcapi = WooCommerce.get_instance()
        data = self.model_dump()
        response = wcapi.put(f"products/categories/{self.id}", data) if self.id else wcapi.post("products/categories", data)
        
        print(response.json())
        if response.status_code in [200, 201]:
            updated_category = self.model_validate(response.json())
            for field, value in updated_category.model_dump().items():
                setattr(self, field, value)
            return self
        
        raise Exception(response.json().get("message", "Unknown error"))

    def delete(self):
        """
        Delete the category from WooCommerce.
        """
        if not self.id:
            raise Exception("Category has no ID. Cannot delete.")
        
        wcapi = WooCommerce.get_instance()
        response = wcapi.delete(f"products/categories/{self.id}")
        return response.json()

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, slug={self.slug}, product_count={self.count})"
