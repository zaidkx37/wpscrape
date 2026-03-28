"""
wpscrape - WordPress/WooCommerce store scraper SDK.

Quick start::

    from wpscrape import WordPress

    wp = WordPress('boskistores.com')
    products = wp.products()
    categories = wp.categories()

"""

from wpscrape.client import WordPress
from wpscrape.exceptions import (
    CategoryNotFoundError,
    ParsingError,
    ProductNotFoundError,
    RateLimitError,
    RequestError,
    SiteNotFoundError,
    WPScrapeError,
)
from wpscrape.exporter import Exporter
from wpscrape.models import (
    Category,
    PaginatedResponse,
    Product,
    ProductAttribute,
    ProductBrand,
    ProductCategory,
    ProductImage,
    ProductPrice,
    SiteInfo,
)

__version__ = '0.1.1'

__all__ = [
    # Client
    'WordPress',
    # Export
    'Exporter',
    # Exceptions
    'WPScrapeError',
    'SiteNotFoundError',
    'ProductNotFoundError',
    'CategoryNotFoundError',
    'RateLimitError',
    'RequestError',
    'ParsingError',
    # Models
    'SiteInfo',
    'Product',
    'ProductPrice',
    'ProductImage',
    'ProductCategory',
    'ProductBrand',
    'ProductAttribute',
    'Category',
    'PaginatedResponse',
]
