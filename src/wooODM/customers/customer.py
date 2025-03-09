from pydantic import BaseModel, Field, EmailStr
from typing import Dict, Optional, List, Any
from datetime import datetime
from wooODM.core import WooBasicODM

class BillingProperties(BaseModel):
    first_name: Optional[str] = None  # First name.
    last_name: Optional[str] = None  # Last name.
    company: Optional[str] = None  # Company name.
    address_1: Optional[str] = None  # Address line 1
    address_2: Optional[str] = None  # Address line 2
    city: Optional[str] = None  # City name.
    state: Optional[str] = None  # ISO code or name of the state, province or district.
    postcode: Optional[str] = None  # Postal code.
    country: Optional[str] = None  # ISO code of the country.
    email: Optional[str] = None  # Email address.
    phone: Optional[str] = None  # Phone number.

class ShippingProperties(BaseModel):
    first_name: Optional[str] = None  # First name.
    last_name: Optional[str] = None  # Last name.
    company: Optional[str] = None  # Company name.
    address_1: Optional[str] = None  # Address line 1
    address_2: Optional[str] = None  # Address line 2
    city: Optional[str] = None  # City name.
    state: Optional[str] = None  # ISO code or name of the state, province or district.
    postcode: Optional[str] = None  # Postal code.
    country: Optional[str] = None  # ISO code of the country.

class MetaDataProperties(BaseModel):
    id: Optional[int] = None  # Meta ID. read-only
    key: Optional[str] = None  # Meta key.
    value: Optional[str] = None  # Meta value.

class Customer(WooBasicODM):
    id: Optional[int] = None  # Unique identifier for the resource. read-only
    date_created: Optional[datetime] = None  # The date the customer was created, in the site's timezone. read-only
    date_created_gmt: Optional[datetime] = None  # The date the customer was created, as GMT. read-only
    date_modified: Optional[datetime] = None  # The date the customer was last modified, in the site's timezone. read-only
    date_modified_gmt: Optional[datetime] = None  # The date the customer was last modified, as GMT. read-only
    email: EmailStr  # The email address for the customer. mandatory
    first_name: Optional[str] = None  # Customer first name.
    last_name: Optional[str] = None  # Customer last name.
    role: Optional[str] = None  # Customer role. read-only
    username: str  # Customer login name.
    password: Optional[str] = None  # Customer password. write-only
    billing: Optional[BillingProperties] = None  # List of billing address data. See Customer - Billing properties
    shipping: Optional[ShippingProperties] = None  # List of shipping address data. See Customer - Shipping properties
    is_paying_customer: Optional[bool] = None  # Is the customer a paying customer? read-only
    avatar_url: Optional[str] = None  # Avatar URL. read-only
    meta_data: List[MetaDataProperties] = Field(default=[])  # Meta data. See Customer - Meta data properties
    
    def save(self):
        """
        Overrides the save method to handle edge cases
        """
        # For some reason, the customer returned from the API may have an empty email field for the billing details
        # in this case, saving the customer will fail

        # Firstly, skip if billing not in the object
        if not self.billing:
            return super().save()
        
        # Secondly, save right away if the email is not empty
        if self.billing.email and self.billing.email != "":
            return super().save()
        
        # Then, check if the email is empty
        if not self.billing.email or self.billing.email == "":
            # Lastly, raise an exception when the object has some data edited, but not the email
            for field in self.billing.model_dump().values():
                if field and field != "":
                    raise Exception("It seems you edited the billing details of a customer, but did not provide an email for the billing details. " \
                    "Please provide an email address in order to succesfully save the customer's billing details.")
            
            # Otherwise, save the customer without saving the billing details
            self.billing = None # (this will not affect the returned object, as it gets updated after saving)
            return super().save()
        
        # If the code reached here, something went wrong
        raise Exception("An unexpected error occurred while trying to save the customer. Please create an issue on the GitHub repository (it would be of huge help :)).")
    
    @classmethod
    def endpoint(cls, id: int = None) -> str:
        return "customers" if id is None else f"customers/{id}"

    def __repr__(self):
        return f"Customer(id={self.id}, email={self.email}, first_name={self.first_name}, last_name={self.last_name})"