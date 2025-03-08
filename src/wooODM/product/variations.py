from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Any
from datetime import datetime
from ..core import WooBasicODM

class VariationDimensions(BaseModel):
    length: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None

class VariationDownload(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    file: Optional[str] = None

class VariationAttribute(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    option: Optional[str] = None

class VariationImage(BaseModel):
    id: Optional[int] = None  # Image ID
    date_created: Optional[datetime] = None  # The date the image was created, in the site's timezone (read-only)
    date_created_gmt: Optional[datetime] = None  # The date the image was created, as GMT (read-only)
    date_modified: Optional[datetime] = None  # The date the image was last modified, in the site's timezone (read-only)
    date_modified_gmt: Optional[datetime] = None  # The date the image was last modified, as GMT (read-only)
    src: Optional[str] = None  # Image URL
    name: Optional[str] = None  # Image name
    alt: Optional[str] = None  # Image alternative text

class VariationMetaData(BaseModel):
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    key: Optional[str] = None  # Meta key
    value: Optional[Any] = None  # Meta value

class ProductVariation(WooBasicODM):
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    date_created: Optional[datetime] = None  # The date the variation was created, in the site's timezone (read-only)
    date_created_gmt: Optional[datetime] = None  # The date the variation was created, as GMT (read-only)
    date_modified: Optional[datetime] = None  # The date the variation was last modified, in the site's timezone (read-only)
    date_modified_gmt: Optional[datetime] = None  # The date the variation was last modified, as GMT (read-only)
    description: Optional[str] = None  # Variation description
    permalink: Optional[str] = None  # Variation URL (read-only)
    sku: Optional[str] = None  # Unique identifier
    price: Optional[str] = None  # Current variation price (read-only)
    regular_price: Optional[str] = None  # Variation regular price
    sale_price: Optional[str] = None  # Variation sale price
    date_on_sale_from: Optional[datetime] = None  # Start date of sale price, in the site's timezone
    date_on_sale_from_gmt: Optional[datetime] = None  # Start date of sale price, as GMT
    date_on_sale_to: Optional[datetime] = None  # End date of sale price, in the site's timezone
    date_on_sale_to_gmt: Optional[datetime] = None  # End date of sale price, as GMT
    on_sale: Optional[bool] = None  # Shows if the variation is on sale (read-only)
    status: str = "publish"  # Variation status
    purchasable: Optional[bool] = None  # Shows if the variation can be bought (read-only)
    virtual: bool = False  # If the variation is virtual
    downloadable: bool = False  # If the variation is downloadable
    downloads: List[VariationDownload] = Field(default=[])  # List of downloadable files
    download_limit: int = -1  # Number of times downloadable files can be downloaded after purchase
    download_expiry: int = -1  # Number of days until access to downloadable files expires
    tax_status: str = "taxable"  # Tax status
    tax_class: Optional[str] = None  # Tax class
    manage_stock: bool = False  # Stock management at variation level
    stock_quantity: Optional[int] = None  # Stock quantity
    stock_status: str = "instock"  # Controls the stock status of the product
    backorders: str = "no"  # If managing stock, this controls if backorders are allowed
    backorders_allowed: Optional[bool] = None  # Shows if backorders are allowed (read-only)
    backordered: Optional[bool] = None  # Shows if the variation is on backordered (read-only)
    weight: Optional[str] = None  # Variation weight
    dimensions: Optional[VariationDimensions] = None  # Variation dimensions
    shipping_class: Optional[str] = None  # Shipping class slug
    shipping_class_id: Optional[int] = None  # Shipping class ID (read-only)
    image: Optional[VariationImage] = None  # Variation image data
    attributes: List[VariationAttribute] = Field(default=[])  # List of attributes
    menu_order: int = 0  # Menu order, used to custom sort products
    meta_data: List[VariationMetaData] = Field(default=[])  # Meta data

    @classmethod
    def endpoint(cls, id: int = None) -> str:
        assert id is not None, "Variation ID is mandatory"

        return f"products/{id}/variations/"
    
    @classmethod
    def model_validate(cls, data: Dict[str, Any]) -> "ProductVariation":
        """
        Override the model_validate method to handle nested objects.
        """
        # Call the super method first
        validated_object = super().model_validate(data)
        
        # Validate and parse nested objects
        if "downloads" in validated_object:
            validated_object["downloads"] = [VariationDownload.model_validate(download) for download in validated_object["downloads"]]
        if "dimensions" in validated_object:
            validated_object["dimensions"] = VariationDimensions.model_validate(validated_object["dimensions"])
        if "image" in validated_object:
            validated_object["image"] = VariationImage.model_validate(validated_object["image"])
        if "attributes" in validated_object:
            validated_object["attributes"] = [VariationAttribute.model_validate(attribute) for attribute in validated_object["attributes"]]
        if "meta_data" in validated_object:
            validated_object["meta_data"] = [VariationMetaData.model_validate(meta) for meta in validated_object["meta_data"]]
        
        return validated_object

    def __repr__(self):
        return f"ProductVariation(id={self.id}, sku={self.sku}, price={self.price}, stock={self.stock_quantity})"