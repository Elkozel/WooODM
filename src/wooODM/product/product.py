from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime  # Correct import for datetime

class Product(BaseModel):
    """
    Represents a WooCommerce product using Pydantic for validation & deserialization.
    """
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    name: str  # Product name
    slug: str  # Product slug
    permalink: Optional[str] = None  # Product URL (read-only)
    date_created: Optional[datetime] = None  # Date product created (site's timezone)
    date_created_gmt: Optional[datetime] = None  # Date product created (GMT)
    date_modified: Optional[datetime] = None  # Date product last modified (site's timezone)
    date_modified_gmt: Optional[datetime] = None  # Date product last modified (GMT)
    type: str = "simple"  # Product type (default is 'simple')
    status: str = "publish"  # Product status (default is 'publish')
    featured: bool = False  # Featured product (default is False)
    catalog_visibility: str = "visible"  # Catalog visibility (default is 'visible')
    description: Optional[str] = None  # Product description
    short_description: Optional[str] = None  # Product short description
    sku: Optional[str] = None  # Unique identifier (SKU)
    price: Optional[str] = None  # Current product price (read-only)
    regular_price: Optional[str] = None  # Product regular price
    sale_price: Optional[str] = None  # Product sale price
    date_on_sale_from: Optional[datetime] = None  # Sale price start date
    date_on_sale_from_gmt: Optional[datetime] = None  # Sale price start date (GMT)
    date_on_sale_to: Optional[datetime] = None  # Sale price end date
    date_on_sale_to_gmt: Optional[datetime] = None  # Sale price end date (GMT)
    price_html: Optional[str] = None  # Price formatted in HTML (read-only)
    on_sale: Optional[bool] = None  # If the product is on sale (read-only)
    purchasable: Optional[bool] = None  # If the product can be purchased (read-only)
    total_sales: Optional[int] = None  # Amount of sales (read-only)
    virtual: bool = False  # Whether the product is virtual (default is False)
    downloadable: bool = False  # Whether the product is downloadable (default is False)
    downloads: List[Dict[str, Any]] = Field(default=[])  # List of downloadable files
    download_limit: int = -1  # Number of times downloadable files can be downloaded (default is -1)
    download_expiry: int = -1  # Number of days until access to downloadable files expires (default is -1)
    external_url: Optional[str] = None  # Product external URL (for external products)
    button_text: Optional[str] = None  # Product external button text (for external products)
    tax_status: str = "taxable"  # Tax status (default is 'taxable')
    tax_class: Optional[str] = None  # Tax class
    manage_stock: bool = False  # If stock is managed at the product level (default is False)
    stock_quantity: Optional[int] = None  # Stock quantity
    stock_status: str = "instock"  # Stock status (default is 'instock')
    backorders: str = "no"  # If backorders are allowed (default is 'no')
    backorders_allowed: Optional[bool] = None  # If backorders are allowed (read-only)
    backordered: Optional[bool] = None  # If the product is backordered (read-only)
    sold_individually: bool = False  # Allow one item per order (default is False)
    weight: Optional[str] = None  # Product weight
    dimensions: Optional[Dict[str, Any]] = None  # Product dimensions
    shipping_required: Optional[bool] = None  # Whether the product requires shipping (read-only)
    shipping_taxable: Optional[bool] = None  # Whether product shipping is taxable (read-only)
    shipping_class: Optional[str] = None  # Shipping class slug
    shipping_class_id: Optional[int] = None  # Shipping class ID (read-only)
    reviews_allowed: bool = True  # Allow reviews (default is True)
    average_rating: Optional[str] = None  # Reviews average rating (read-only)
    rating_count: Optional[int] = None  # Amount of reviews the product has (read-only)
    related_ids: List[int] = Field(default=[])  # List of related product IDs (read-only)
    upsell_ids: List[int] = Field(default=[])  # List of upsell product IDs
    cross_sell_ids: List[int] = Field(default=[])  # List of cross-sell product IDs
    parent_id: Optional[int] = None  # Product parent ID
    purchase_note: Optional[str] = None  # Optional note after purchase
    categories: List[Dict[str, Any]] = Field(default=[])  # List of categories
    tags: List[Dict[str, Any]] = Field(default=[])  # List of tags
    images: List[Dict[str, Any]] = Field(default=[])  # List of images
    attributes: List[Dict[str, Any]] = Field(default=[])  # List of attributes
    default_attributes: List[Dict[str, Any]] = Field(default=[])  # Default variation attributes
    variations: List[int] = Field(default=[])  # List of variation IDs (read-only)
    grouped_products: List[int] = Field(default=[])  # List of grouped product IDs
    menu_order: int = 0  # Menu order for sorting products
    meta_data: List[Dict[str, Any]] = Field(default=[])  # List of meta data

    @classmethod
    def all(cls, per_page: int = 10, page: int = 1):
        """
        Fetch all products with pagination and return a list of Product objects.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(f"products?per_page={per_page}&page={page}").json()
        
        if response:
            return [cls.model_validate(product) for product in response]
        
        return []  # If no products are found, return an empty list

    def save(self):
        """
        Save the product to WooCommerce. Updates if it has an ID, otherwise creates a new one.
        """
        wcapi = WooCommerce.get_instance()
        data = self.model_dump()
        response = wcapi.put(f"products/{self.id}", data) if self.id else wcapi.post("products", data)
        
        if response.status_code in [200, 201]:
            updated_product = self.model_validate(response.json())
            for field, value in updated_product.model_dump().items():
                setattr(self, field, value)
            return self
        
        raise Exception(response.json().get("message", "Unknown error"))

    def delete(self):
        """
        Delete the product from WooCommerce.
        """
        if not self.id:
            raise Exception("Product has no ID. Cannot delete.")
        
        wcapi = WooCommerce.get_instance()
        response = wcapi.delete(f"products/{self.id}")
        return response.json()

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, sku={self.sku}, price={self.price}, stock={self.stock_quantity})"
