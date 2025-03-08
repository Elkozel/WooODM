# WooODM

WooODM is a project designed to provide an Object-Document Mapper (ODM) for WooCommerce, allowing easy interaction with the WooCommerce API using Python.

## Installation

To install WooODM locally as a package, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/WooODM.git
    ```
2. Navigate to the project directory:
    ```sh
    cd WooODM
    ```
3. Install the package locally:
    ```sh
    pip install .
    ```
    
    ### Running for Development

    To run WooODM for development purposes, follow these steps:

    1. Install the package in editable mode:
        ```sh
        pip install -e .
        ```
## Usage

To start using WooODM, follow these steps:

1. Initialize the WooCommerce API:
    ```python
    from wooODM.core import WooCommerce

    WooCommerce.init(url="your_store_url", consumer_key="your_consumer_key", consumer_secret="your_consumer_secret")
    ```

2. Use the provided models to interact with WooCommerce:
    ```python
    from wooODM.product.product import Product

    # Fetch all products
    products = Product.all()

    # Get a specific product by ID
    product = Product.get(product_id=123)

    # Create a new product
    new_product = Product(name="New Product", regular_price="19.99")
    new_product.save()
    ```

## Contributing
For guidelines on how to contribute to WooODM, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.