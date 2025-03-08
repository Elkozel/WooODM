from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from wooODM.core import WooBasicODM, WooCommerce

class DownloadProperties(BaseModel):
    id: Optional[str] = None  # File ID
    name: Optional[str] = None  # File name
    file: Optional[str] = None  # File URL

class DimensionsProperties(BaseModel):
    length: Optional[str] = None  # Product length
    width: Optional[str] = None  # Product width
    height: Optional[str] = None  # Product height

class CategoryProperties(BaseModel):
    id: Optional[int] = None  # Category ID
    name: Optional[str] = None  # Category name (read-only)
    slug: Optional[str] = None  # Category slug (read-only)

class TagProperties(BaseModel):
    id: Optional[int] = None  # Tag ID
    name: Optional[str] = None  # Tag name (read-only)
    slug: Optional[str] = None  # Tag slug (read-only)

class ImageProperties(BaseModel):
    id: Optional[int] = None  # Attachment ID from Media Library
    date_created: Optional[datetime] = None  # Date image created (site's timezone, read-only)
    date_created_gmt: Optional[datetime] = None  # Date image created (GMT, read-only)
    date_modified: Optional[datetime] = None  # Date image last modified (site's timezone, read-only)
    date_modified_gmt: Optional[datetime] = None  # Date image last modified (GMT, read-only)
    src: Optional[str] = None  # Image URL
    name: Optional[str] = None  # Image name
    alt: Optional[str] = None  # Image alternative text

class AttributeProperties(BaseModel):
    id: Optional[int] = None  # Attribute ID
    name: Optional[str] = None  # Attribute name
    position: Optional[int] = None  # Attribute position
    visible: bool = None  # If attribute is visible on product page (default is False)
    variation: bool = None  # If attribute can be used as variation (default is False)
    options: List[str] = Field(default=[])  # List of available term names

class DefaultAttributeProperties(BaseModel):
    id: Optional[int] = None  # Attribute ID
    name: Optional[str] = None  # Attribute name
    option: Optional[str] = None  # Selected attribute term name

class MetaDataProperties(BaseModel):
    id: Optional[int] = None  # Meta ID (read-only)
    key: Optional[str] = None  # Meta key
    value: Optional[Any] = None  # Meta value

class Product(WooBasicODM):
    """
    Represents a WooCommerce product using Pydantic for validation & deserialization.
    """
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    name: str  # Product name
    slug: Optional[str] = None  # Product slug
    permalink: Optional[str] = None  # Product URL (read-only)
    date_created: Optional[datetime] = None  # Date product created (site's timezone, read-only)
    date_created_gmt: Optional[datetime] = None  # Date product created (GMT, read-only)
    date_modified: Optional[datetime] = None  # Date product last modified (site's timezone, read-only)
    date_modified_gmt: Optional[datetime] = None  # Date product last modified (GMT, read-only)
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
    downloads: List[DownloadProperties] = Field(default=[])  # List of downloadable files
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
    dimensions: Optional[DimensionsProperties] = None  # Product dimensions
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
    categories: List[CategoryProperties] = Field(default=[])  # List of categories
    tags: List[TagProperties] = Field(default=[])  # List of tags
    images: List[ImageProperties] = Field(default=[])  # List of images
    attributes: List[AttributeProperties] = Field(default=[])  # List of attributes
    default_attributes: List[DefaultAttributeProperties] = Field(default=[])  # Default variation attributes
    variations: List[int] = Field(default=[])  # List of variation IDs (read-only)
    grouped_products: List[int] = Field(default=[])  # List of grouped product IDs
    menu_order: int = 0  # Menu order for sorting products
    meta_data: List[MetaDataProperties] = Field(default=[])  # List of meta data

    def save(self):
        """
        Save the product to WooCommerce. Updates if it has an ID, otherwise creates a new one.
        """
        # Save categories and tags first
        for category in self.categories:
            category.save()
        for tag in self.tags:
            tag.save()
        
        # Then proceed with the product
        return super().save()

    @classmethod
    def endpoint(cls, id: int = None) -> str:
        return "products" if id is None else f"products/{id}"

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, sku={self.sku}, price={self.price}, stock={self.stock_quantity})"