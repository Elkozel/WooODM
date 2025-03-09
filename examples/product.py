from wooODM.core import WooCommerce
from wooODM.products.product import Product

# Initialize the API
url = ""
consumer_key = ""
consumer_secret = ""
WooCommerce.init(url, consumer_key, consumer_secret)

# Create a product
p = Product(
        name="Awesome Shirt",
        slug="awesome-shirt",
        regular_price="29.99",
        description="A really awesome shirt",
        stock_quantity=20,
    )
p.save()  # once product is saved, ID is assigned automatically
print(p.id)

# Youw can also fetch the product by id
fetched_p = Product.get(p.id)
print(fetched_p)

# Update the product
p.name = "Super Awesome Shirt"
# just remember to save it after
p.save()

# Lastly, you can delete the product
p.delete()

# If you need to add some variations or other properties, all nested classes are also defnied in the product file
from wooODM.products.product import DownloadProperties, DimensionsProperties, CategoryProperties, TagProperties, ImageProperties, AttributeProperties, DefaultAttributeProperties, MetaDataProperties
p.downloads.append(DownloadProperties(id="download1", name="Download 1", file="http://example.com/download1"))
p.dimensions = DimensionsProperties(length="10", width="5", height="2")
p.save()