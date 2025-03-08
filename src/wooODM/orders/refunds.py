from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from wooODM.core import WooDoubleIdODM

class MetaDataProperties(BaseModel):
    id: Optional[int] = None  # Meta ID (read-only)
    key: Optional[str] = None  # Meta key
    value: Optional[Any] = None  # Meta value

class LineItemTaxProperties(BaseModel):
    id: Optional[int] = None  # Tax rate ID (read-only)
    total: Optional[str] = None  # Tax total (read-only)
    subtotal: Optional[str] = None  # Tax subtotal (read-only)

class LineItemProperties(BaseModel):
    id: Optional[int] = None  # Item ID (read-only)
    name: Optional[str] = None  # Product name
    product_id: Optional[int] = None  # Product ID
    variation_id: Optional[int] = None  # Variation ID, if applicable
    quantity: Optional[int] = None  # Quantity ordered
    tax_class: Optional[str] = None  # Tax class of product
    subtotal: Optional[str] = None  # Line subtotal (before discounts)
    subtotal_tax: Optional[str] = None  # Line subtotal tax (before discounts) (read-only)
    total: Optional[str] = None  # Line total (after discounts)
    total_tax: Optional[str] = None  # Line total tax (after discounts) (read-only)
    taxes: List[LineItemTaxProperties] = Field(default=[])  # Line taxes (read-only)
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data
    sku: Optional[str] = None  # Product SKU (read-only)
    price: Optional[str] = None  # Product price (read-only)
    
class TaxLineProperties(BaseModel):
    id: Optional[int] = None  # Item ID (read-only)
    rate_code: Optional[str] = None  # Tax rate code (read-only)
    rate_id: Optional[int] = None  # Tax rate ID (read-only)
    label: Optional[str] = None  # Tax rate label (read-only)
    compound: Optional[bool] = None  # Whether or not this is a compound tax rate (read-only)
    tax_total: Optional[str] = None  # Tax total (not including shipping taxes) (read-only)
    shipping_tax_total: Optional[str] = None  # Shipping tax total (read-only)
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data

class ShippingLineProperties(BaseModel):
    id: Optional[int] = None  # Item ID (read-only)
    method_title: Optional[str] = None  # Shipping method name
    method_id: Optional[str] = None  # Shipping method ID
    total: Optional[str] = None  # Line total (after discounts)
    total_tax: Optional[str] = None  # Line total tax (after discounts) (read-only)
    taxes: List[TaxLineProperties] = Field(default=[])  # Line taxes (read-only)
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data

class FeeLineProperties(BaseModel):
    id: Optional[int] = None  # Item ID (read-only)
    name: Optional[str] = None  # Fee name
    tax_class: Optional[str] = None  # Tax class of fee
    tax_status: Optional[str] = None  # Tax status of fee (Options: taxable and none)
    total: Optional[str] = None  # Line total (after discounts)
    total_tax: Optional[str] = None  # Line total tax (after discounts) (read-only)
    taxes: List[TaxLineProperties] = Field(default=[])  # Line taxes (read-only)
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data

class Refund(WooDoubleIdODM):
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    date_created: Optional[datetime] = None  # The date the order refund was created (site's timezone) (read-only)
    date_created_gmt: Optional[datetime] = None  # The date the order refund was created (GMT) (read-only)
    amount: Optional[str] = None  # Total refund amount
    reason: Optional[str] = None  # Reason for refund
    refunded_by: Optional[int] = None  # User ID of user who created the refund
    refunded_payment: Optional[bool] = None  # If the payment was refunded via the API (read-only)
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data
    line_items: List[LineItemProperties] = Field(default=[])  # Line items data
    tax_lines: List[TaxLineProperties] = Field(default=[])  # Tax lines data (read-only)
    shipping_lines: List[ShippingLineProperties] = Field(default=[])  # Shipping lines data
    fee_lines: List[FeeLineProperties] = Field(default=[])  # Fee lines data
    api_refund: bool = True  # When true, the payment gateway API is used to generate the refund (write-only)
    api_restock: bool = True  # When true, the selected line items are restocked (write-only)

    @classmethod
    def endpoint(cls, id1: int, id2: int = None) -> str:
        assert id1 is not None, "Order ID is mandatory"
        return f"orders/{id1}/refunds/{id2}" if id2 else f"orders/{id1}/refunds/"

    def __repr__(self):
        return f"Refund(id={self.id}, amount={self.amount}, reason={self.reason})"