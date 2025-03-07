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
