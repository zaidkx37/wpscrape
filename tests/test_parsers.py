"""Tests for response parsers."""

from wpscrape._parsers import parse_category, parse_product, parse_site_info


def test_parse_site_info():
    data = {
        'name': 'Test Store',
        'description': 'A test store',
        'url': 'https://test.com',
        'namespaces': ['wp/v2', 'wc/store/v1', 'wc/v3'],
    }
    site = parse_site_info(data)
    assert site.name == 'Test Store'
    assert site.has_woocommerce is True


def test_parse_site_info_no_woo():
    data = {
        'name': 'Blog',
        'description': 'Just a blog',
        'url': 'https://blog.com',
        'namespaces': ['wp/v2'],
    }
    site = parse_site_info(data)
    assert site.has_woocommerce is False


def test_parse_product_minimal():
    data = {
        'id': 123,
        'name': 'Widget',
        'slug': 'widget',
        'permalink': 'https://store.com/product/widget',
        'type': 'simple',
        'on_sale': True,
        'is_in_stock': True,
        'prices': {
            'price': '1500',
            'regular_price': '2000',
            'sale_price': '1500',
            'currency_code': 'PKR',
            'currency_symbol': '₨',
            'currency_minor_unit': 0,
        },
    }
    product = parse_product(data)
    assert product.id == 123
    assert product.name == 'Widget'
    assert product.on_sale is True
    assert product.price == 1500.0
    assert product.regular_price == 2000.0
    assert product.prices.discount_percentage == 25.0


def test_parse_product_with_categories():
    data = {
        'id': 456,
        'name': 'Earbuds Pro',
        'slug': 'earbuds-pro',
        'categories': [
            {'id': 150, 'name': 'Earbuds', 'slug': 'earbuds'},
            {'id': 147, 'name': 'Best Sellers', 'slug': 'best-sellers'},
        ],
        'images': [
            {'id': 1, 'src': 'https://img.com/1.jpg', 'thumbnail': 'https://img.com/1t.jpg',
             'name': 'main', 'alt': 'Earbuds'},
        ],
    }
    product = parse_product(data)
    assert len(product.categories) == 2
    assert product.category_names == ['Earbuds', 'Best Sellers']
    assert product.primary_image == 'https://img.com/1.jpg'


def test_parse_category():
    data = {
        'id': 150,
        'name': 'Earbuds',
        'slug': 'earbuds',
        'count': 33,
        'parent': 0,
        'description': 'Wireless earbuds',
    }
    cat = parse_category(data)
    assert cat.id == 150
    assert cat.name == 'Earbuds'
    assert cat.count == 33
    assert cat.url == '/product-category/earbuds'
