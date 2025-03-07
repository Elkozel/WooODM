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
    
class WooBasicODM(BaseModel):
    """
    Abstract base class for WooCommerce models.
    """
    
    @classmethod
    @abstractmethod
    def endpoint(cls) -> str:
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
        response = wcapi.get(f"{cls.endpoint()}?per_page={per_page}&page={page}")

        if response.status_code == 200:
            return [cls.model_validate(item) for item in response.json()]
        
        raise Exception(response.json().get("message", "Unknown error"))
    
    @classmethod
    def get(cls, item_id: int):
        """
        Retrieve an item from WooCommerce by ID and return a model object.
        """
        wcapi = WooCommerce.get_instance()
        response = wcapi.get(f"{cls.endpoint()}/{item_id}")
        
        if response.status_code == 200:
            return cls.model_validate(response.json())
        
        raise Exception(response.json().get("message", "Unknown error"))

    def save(self):
        """
        Save the item to WooCommerce. Updates if it has an ID, otherwise creates a new one.
        """
        wcapi = WooCommerce.get_instance()
        data = self.model_dump()
        response = wcapi.put(f"{self.endpoint()}/{self.id}", data) if self.id else wcapi.post(self.endpoint(), data)
        
        if response.status_code in [200, 201]:
            updated_item = self.model_validate(response.json())
            for field, value in updated_item.model_dump().items():
                setattr(self, field, value)
            return self
        
        raise Exception(response.json().get("message", "Unknown error"))

    def delete(self):
        """
        Delete the item from WooCommerce.
        """
        if not self.id:
            raise Exception("Item has no ID. Cannot delete.")
        
        wcapi = WooCommerce.get_instance()
        response = wcapi.delete(f"{self.endpoint()}/{self.id}")
        return response.json()