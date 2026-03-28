"""Tests for URL builders."""

from wpscrape._endpoints import (
    api_index_url,
    categories_url,
    normalize_domain,
    product_by_slug_url,
    products_by_category_url,
    products_search_url,
    products_url,
)


def test_normalize_domain_plain():
    assert normalize_domain('boskistores.com') == 'https://boskistores.com'


def test_normalize_domain_with_www():
    assert normalize_domain('www.boskistores.com') == 'https://www.boskistores.com'


def test_normalize_domain_with_https():
    assert normalize_domain('https://boskistores.com') == 'https://boskistores.com'


def test_normalize_domain_strips_trailing_slash():
    assert normalize_domain('https://boskistores.com/') == 'https://boskistores.com'


def test_api_index_url():
    assert api_index_url('https://example.com') == 'https://example.com/wp-json/'


def test_products_url_defaults():
    url = products_url('https://example.com')
    assert url == 'https://example.com/wp-json/wc/store/v1/products?page=1&per_page=100'


def test_products_url_custom():
    url = products_url('https://example.com', page=3, per_page=50)
    assert url == 'https://example.com/wp-json/wc/store/v1/products?page=3&per_page=50'


def test_product_by_slug_url():
    url = product_by_slug_url('https://example.com', 'cool-widget')
    assert url == 'https://example.com/wp-json/wc/store/v1/products?slug=cool-widget'


def test_products_by_category_url():
    url = products_by_category_url('https://example.com', 150, page=2, per_page=30)
    assert url == 'https://example.com/wp-json/wc/store/v1/products?category=150&page=2&per_page=30'


def test_products_search_url():
    url = products_search_url('https://example.com', 'watch')
    assert url == 'https://example.com/wp-json/wc/store/v1/products?search=watch&page=1&per_page=100'


def test_categories_url():
    url = categories_url('https://example.com')
    assert url == 'https://example.com/wp-json/wc/store/v1/products/categories'
