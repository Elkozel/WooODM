from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from wooODM.core import WooBasicODM

class BillingProperties(BaseModel):
    first_name: Optional[str] = None  # First name
    last_name: Optional[str] = None  # Last name
    company: Optional[str] = None  # Company name
    address_1: Optional[str] = None  # Address line 1
    address_2: Optional[str] = None  # Address line 2
    city: Optional[str] = None  # City name
    state: Optional[str] = None  # ISO code or name of the state, province or district
    postcode: Optional[str] = None  # Postal code
    country: Optional[str] = None  # Country code in ISO 3166-1 alpha-2 format
    email: Optional[str] = None  # Email address
    phone: Optional[str] = None  # Phone number

class ShippingProperties(BaseModel):
    first_name: Optional[str] = None  # First name
    last_name: Optional[str] = None  # Last name
    company: Optional[str] = None  # Company name
    address_1: Optional[str] = None  # Address line 1
    address_2: Optional[str] = None  # Address line 2
    city: Optional[str] = None  # City name
    state: Optional[str] = None  # ISO code or name of the state, province or district
    postcode: Optional[str] = None  # Postal code
    country: Optional[str] = None  # Country code in ISO 3166-1 alpha-2 format

class MetaDataProperties(BaseModel):
    id: Optional[int] = None  # Meta ID (read-only)
    key: Optional[str] = None  # Meta key
    value: Optional[Any] = None  # Meta value

class LineItemProperties(BaseModel):
    id: Optional[int] = None  # Item ID (read-only)
    name: Optional[str] = None  # Product name
    product_id: Optional[int] = None  # Product ID
    variation_id: Optional[int] = None  # Variation ID, if applicable
    quantity: Optional[int] = None  # Quantity ordered
    tax_class: Optional[str] = None  # Slug of the tax class of product
    subtotal: Optional[str] = None  # Line subtotal (before discounts)
    subtotal_tax: Optional[str] = None  # Line subtotal tax (before discounts) (read-only)
    total: Optional[str] = None  # Line total (after discounts)
    total_tax: Optional[str] = None  # Line total tax (after discounts) (read-only)
    taxes: List[Dict[str, Any]] = Field(default=[])  # Line taxes (read-only)
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
    taxes: List[Dict[str, Any]] = Field(default=[])  # Line taxes (read-only)
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data

class FeeLineProperties(BaseModel):
    id: Optional[int] = None  # Item ID (read-only)
    name: Optional[str] = None  # Fee name
    tax_class: Optional[str] = None  # Tax class of fee
    tax_status: Optional[str] = None  # Tax status of fee (Options: taxable and none)
    total: Optional[str] = None  # Line total (after discounts)
    total_tax: Optional[str] = None  # Line total tax (after discounts) (read-only)
    taxes: List[Dict[str, Any]] = Field(default=[])  # Line taxes (read-only)
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data

class CouponLineProperties(BaseModel):
    id: Optional[int] = None  # Item ID (read-only)
    code: Optional[str] = None  # Coupon code
    discount: Optional[str] = None  # Discount total (read-only)
    discount_tax: Optional[str] = None  # Discount total tax (read-only)
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data

class RefundProperties(BaseModel):
    id: Optional[int] = None  # Refund ID (read-only)
    reason: Optional[str] = None  # Refund reason (read-only)
    total: Optional[str] = None  # Refund total (read-only)

class Order(WooBasicODM):
    id: Optional[int] = None  # Unique identifier for the resource (read-only)
    parent_id: Optional[int] = None  # Parent order ID
    number: Optional[str] = None  # Order number (read-only)
    order_key: Optional[str] = None  # Order key (read-only)
    created_via: Optional[str] = None  # Shows where the order was created (read-only)
    version: Optional[str] = None  # Version of WooCommerce which last updated the order (read-only)
    status: str = "pending"  # Order status (default is 'pending')
    currency: str = "USD"  # Currency the order was created with (default is 'USD')
    date_created: Optional[datetime] = None  # The date the order was created (site's timezone) (read-only)
    date_created_gmt: Optional[datetime] = None  # The date the order was created (GMT) (read-only)
    date_modified: Optional[datetime] = None  # The date the order was last modified (site's timezone) (read-only)
    date_modified_gmt: Optional[datetime] = None  # The date the order was last modified (GMT) (read-only)
    discount_total: Optional[str] = None  # Total discount amount for the order (read-only)
    discount_tax: Optional[str] = None  # Total discount tax amount for the order (read-only)
    shipping_total: Optional[str] = None  # Total shipping amount for the order (read-only)
    shipping_tax: Optional[str] = None  # Total shipping tax amount for the order (read-only)
    cart_tax: Optional[str] = None  # Sum of line item taxes only (read-only)
    total: Optional[str] = None  # Grand total (read-only)
    total_tax: Optional[str] = None  # Sum of all taxes (read-only)
    prices_include_tax: Optional[bool] = None  # True if the prices included tax during checkout (read-only)
    customer_id: int = 0  # User ID who owns the order (0 for guests) (default is 0)
    customer_ip_address: Optional[str] = None  # Customer's IP address (read-only)
    customer_user_agent: Optional[str] = None  # User agent of the customer (read-only)
    customer_note: Optional[str] = None  # Note left by customer during checkout
    billing: Optional[BillingProperties] = None  # Billing address
    shipping: Optional[ShippingProperties] = None  # Shipping address
    payment_method: Optional[str] = None  # Payment method ID
    payment_method_title: Optional[str] = None  # Payment method title
    transaction_id: Optional[str] = None  # Unique transaction ID
    date_paid: Optional[datetime] = None  # The date the order was paid (site's timezone) (read-only)
    date_paid_gmt: Optional[datetime] = None  # The date the order was paid (GMT) (read-only)
    date_completed: Optional[datetime] = None  # The date the order was completed (site's timezone) (read-only)
    date_completed_gmt: Optional[datetime] = None  # The date the order was completed (GMT) (read-only)
    cart_hash: Optional[str] = None  # MD5 hash of cart items to ensure orders are not modified (read-only)
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data
    line_items: List[LineItemProperties] = Field(default=[])  # Line items data
    tax_lines: List[TaxLineProperties] = Field(default=[])  # Tax lines data (read-only)
    shipping_lines: List[ShippingLineProperties] = Field(default=[])  # Shipping lines data
    fee_lines: List[FeeLineProperties] = Field(default=[])  # Fee lines data
    coupon_lines: List[CouponLineProperties] = Field(default=[])  # Coupons line data
    refunds: List[RefundProperties] = Field(default=[])  # List of refunds (read-only)
    set_paid: Optional[bool] = None  # Define if the order is paid (write-only)
    
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
    def model_validate(cls, data: Dict[str, Any]) -> "Order":
        """
        Override the model_validate method to handle nested objects.
        """
        # Call the super method first
        validated_object = super().model_validate(data)
        
        # Validate and parse nested objects
        if "billing" in validated_object:
            validated_object["billing"] = [BillingProperties.model_validate(category) for category in validated_object["billing"]]
        if "shipping" in validated_object:
            validated_object["shipping"] = [ShippingProperties.model_validate(tag) for tag in validated_object["shipping"]]
        if "meta_data" in validated_object:
            validated_object["meta_data"] = [MetaDataProperties.model_validate(image) for image in validated_object["meta_data"]]
        if "line_items" in validated_object:
            validated_object["line_items"] = [LineItemProperties.model_validate(attribute) for attribute in validated_object["line_items"]]
        if "tax_lines" in validated_object:
            validated_object["tax_lines"] = [TaxLineProperties.model_validate(default_attribute) for default_attribute in validated_object["tax_lines"]]
        if "shipping_lines" in validated_object:
            validated_object["shipping_lines"] = [ShippingLineProperties.model_validate(download) for download in validated_object["shipping_lines"]]
        if "fee_lines" in validated_object:
            validated_object["fee_lines"] = [FeeLineProperties.model_validate(meta) for meta in validated_object["fee_lines"]]
        if "coupon_lines" in validated_object:
            validated_object["coupon_lines"] = [CouponLineProperties.model_validate(meta) for meta in validated_object["coupon_lines"]]
        if "refunds" in validated_object:
            validated_object["refunds"] = [RefundProperties.model_validate(meta) for meta in validated_object["refunds"]]

        return validated_object

    @classmethod
    def endpoint(cls, id: int = None) -> str:
        return "orders" if id is None else f"orders/{id}"

    def __repr__(self):
        return f"Order(id={self.id}, number={self.number}, total={self.total}, status={self.status})"