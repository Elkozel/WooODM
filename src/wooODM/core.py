import requests
from woocommerce import API  # Install using `pip install woocommerce`

class WooCommerce:
    _instance = None

    def __init__(self, url, consumer_key, consumer_secret):
        self.wcapi = API(
            url=url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            version="wc/v3"
        )

    @classmethod
    def init(cls, url, consumer_key, consumer_secret):
        """
        Initializes the WooCommerce API with credentials.
        """
        if cls._instance is None:
            cls._instance = cls(url, consumer_key, consumer_secret)

    @classmethod
    def get_instance(cls):
        """
        Returns the WooCommerce API instance.
        """
        if cls._instance is None:
            raise Exception("WooCommerce API not initialized. Call WooCommerce.init() first.")
        return cls._instance.wcapi
