"""Tests for data models."""

from wpscrape.models import Product, ProductPrice


def test_product_price_minor_units():
    price = ProductPrice(
        price='150000',
        regular_price='200000',
        sale_price='150000',
        currency_code='PKR',
        currency_symbol='₨',
        currency_minor_unit=2,
    )
    assert price.price_float == 1500.0
    assert price.regular_price_float == 2000.0
    assert price.discount_percentage == 25.0


def test_product_price_no_minor_units():
    price = ProductPrice(
        price='1500',
        regular_price='2000',
        sale_price='1500',
        currency_code='PKR',
        currency_symbol='₨',
        currency_minor_unit=0,
    )
    assert price.price_float == 1500.0
    assert price.regular_price_float == 2000.0


def test_product_to_flat_dict():
    product = Product(
        id=1,
        name='Test Product',
        slug='test-product',
        permalink='https://store.com/product/test-product',
        type='simple',
        sku='TP-001',
        short_description='Short desc',
        description='Long desc',
        on_sale=True,
        is_in_stock=True,
        is_on_backorder=False,
        average_rating='4.5',
        review_count=10,
        prices=ProductPrice(
            price='1000',
            regular_price='1500',
            sale_price='1000',
            currency_code='USD',
            currency_symbol='$',
            currency_minor_unit=0,
        ),
    )
    flat = product.to_flat_dict()
    assert flat['id'] == 1
    assert flat['name'] == 'Test Product'
    assert flat['price'] == 1000.0
    assert flat['on_sale'] is True
    assert flat['currency'] == 'USD'


def test_product_no_prices():
    product = Product(
        id=1, name='No Price', slug='no-price', permalink='', type='simple',
        sku='', short_description='', description='', on_sale=False,
        is_in_stock=False, is_on_backorder=False, average_rating='0', review_count=0,
    )
    assert product.price is None
    assert product.currency is None
    assert product.primary_image is None
