from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod
from woocommerce import API  # Install using `pip install woocommerce`

class WooCommerce:
    """
    A singleton class to interact with the WooCommerce API.
    """
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def init(cls, url, consumer_key, consumer_secret):
        """
        Initializes the WooCommerce API instance.
        Args:
            url (str): The base URL for the WooCommerce store.
            consumer_key (str): The consumer key for the WooCommerce API.
            consumer_secret (str): The consumer secret for the WooCommerce API.
        """
        cls._instance = API(
            url=url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            version="wc/v3"
        )

    @classmethod
    def get_instance(cls):
        """
        Returns the WooCommerce API instance.
        """
        if cls._instance is None:
            raise Exception("WooCommerce API not initialized. Call WooCommerce.init() first.")
        return cls._instance
    
class WooBasicODM(BaseModel, ABC):
    """
    Abstract base class for WooCommerce models.
    """
    
    @classmethod
    @abstractmethod
    def endpoint(cls, id: int = None) -> str:
        """
        Return the endpoint for the WooCommerce model.
        """
        pass

    @classmethod
    def all(cls, per_page: int = 10, page: int = 1):
        """
        Fetch all items with pagination and return a list of model objects.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(f"{cls.endpoint()}", params={"per_page": per_page, "page": page})

        if response.status_code == 200:
            return [cls.model_validate(item) for item in response.json()]
        
        raise Exception(response.json().get("message", "Unknown error"))
    
    @classmethod
    def get(cls, item_id: int):
        """
        Retrieve an item from WooCommerce by ID and return a model object.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(cls.endpoint(item_id))
        
        if response.status_code == 200:
            return cls.model_validate(response.json())
        
        raise Exception(response.json().get("message", "Unknown error"))
    
    def _remove_datetimes(self, data):
        """
        Replace date or datetime objects with their ISO formatted strings, since the datetime cannot be serialized.
        """
        for key, value in data.items():
            if isinstance(value, (datetime, date)):
                data[key] = value.isoformat()
            if isinstance(value, dict):
                data[key] = self._remove_datetimes(value)
        return data

    def save(self):
        """
        Save the item to WooCommerce. Updates if it has an ID, otherwise creates a new one.
        """
        wcapi = WooCommerce.get_instance()
        data = self.model_dump()

        # Datetime objects need to be converted to ISO format before sending
        data = self._remove_datetimes(data)
                
        response = wcapi.put(self.endpoint(self.id), data) if self.id else wcapi.post(self.endpoint(), data)
        
        if response.status_code in [200, 201]:
            response = self.model_validate(response.json())
            self.__dict__.update(response.__dict__)
            return self
        response = response.json()
        errorMsg = response.get("message", "Unknown error")
        errorDetails = response.get("data", {}).get("details", "")
        raise Exception(f"Error: {errorMsg} \n Details: {errorDetails}")

    def delete(self):
        """
        Delete the item from WooCommerce.
        """
        if not self.id:
            raise Exception("Item has no ID. Cannot delete.")
        
        wcapi = WooCommerce.get_instance()
        response = wcapi.delete(self.endpoint(self.id), params={"force": True})
        return self.model_validate(response.json())
    

class WooDoubleIdODM(BaseModel, ABC):
    """
    Abstract base class for WooCommerce models.
    """
    # This is not optional, however it won't work with Pydantic if it's not set to None
    id1: Optional[int] = None # First ID (often of the product or some other parent object)

    @classmethod
    @abstractmethod
    def endpoint(cls, id1: int, id2: int = None) -> str:
        """
        Return the endpoint for the WooCommerce model.
        """
        pass

    @classmethod
    def all(cls, id1: int, per_page: int = 10, page: int = 1):
        """
        Fetch all items with pagination and return a list of model objects.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(f"{cls.endpoint(id1)}", params={"per_page": per_page, "page": page})

        if response.status_code == 200:
            return [cls.model_validate(item) for item in response.json()]
        
        raise Exception(response.json().get("message", "Unknown error"))
    
    @classmethod
    def get(cls, id1: int, id2: int):
        """
        Retrieve an item from WooCommerce by ID and return a model object.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(cls.endpoint(id1, id2))
        
        if response.status_code == 200:
            response_obj = cls.model_validate(response.json())
            response_obj.id1 = id1
            return response_obj
        
        raise Exception(response.json().get("message", "Unknown error"))

    def save(self):
        """
        Save the item to WooCommerce. Updates if it has an ID, otherwise creates a new one.
        """
        assert self.id1 is not None, "ID1 is mandatory for this model."

        wcapi = WooCommerce.get_instance()
        data = self.model_dump()

        # Datetime objects need to be converted to ISO format before sending
        data = self._remove_datetimes(data)

        response = wcapi.put(self.endpoint(self.id1, self.id), data) if self.id else wcapi.post(self.endpoint(self.id1), data)
        
        if response.status_code in [200, 201]:
            response = self.model_validate(response.json())
            self.__dict__.update(response.__dict__)
            return self
        
        errorMsg = response.json().get("message", "Unknown error")
        errorDetails = response.json().get("details", "")
        raise Exception(f"Error: {errorMsg} \n Details: {errorDetails}")

    def delete(self):
        """
        Delete the item from WooCommerce.
        """
        if not self.id:
            raise Exception("Item has no ID. Cannot delete.")
        
        wcapi = WooCommerce.get_instance()
        response = wcapi.delete(self.endpoint(self.id1, self.id), params={"force": True})
        return self.model_validate(response.json())