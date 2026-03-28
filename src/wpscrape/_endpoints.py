"""URL builders for WordPress/WooCommerce REST API endpoints."""

from __future__ import annotations


def normalize_domain(domain: str) -> str:
    """Normalize a domain to 'https://domain' format.

    Accepts:
        'boskistores.com'
        'www.boskistores.com'
        'https://boskistores.com'
        'https://www.boskistores.com/'
    """
    domain = domain.strip().rstrip('/')
    if domain.startswith('http://') or domain.startswith('https://'):
        return domain.rstrip('/')
    return f'https://{domain}'


def api_index_url(base: str) -> str:
    """WP REST API root - site info and available namespaces."""
    return f'{base}/wp-json/'


def products_url(base: str, page: int = 1, per_page: int = 100) -> str:
    """WooCommerce Store API products listing."""
    return f'{base}/wp-json/wc/store/v1/products?page={page}&per_page={per_page}'


def product_by_slug_url(base: str, slug: str) -> str:
    """WooCommerce Store API products filtered by slug."""
    return f'{base}/wp-json/wc/store/v1/products?slug={slug}'


def products_by_category_url(
    base: str, category_id: int, page: int = 1, per_page: int = 100,
) -> str:
    """WooCommerce Store API products filtered by category ID."""
    return (
        f'{base}/wp-json/wc/store/v1/products'
        f'?category={category_id}&page={page}&per_page={per_page}'
    )


def products_search_url(base: str, query: str, page: int = 1, per_page: int = 100) -> str:
    """WooCommerce Store API products search."""
    return f'{base}/wp-json/wc/store/v1/products?search={query}&page={page}&per_page={per_page}'


def categories_url(base: str) -> str:
    """WooCommerce Store API product categories."""
    return f'{base}/wp-json/wc/store/v1/products/categories'


def wp_products_url(base: str, page: int = 1, per_page: int = 100) -> str:
    """WordPress REST API product CPT listing (fallback)."""
    return f'{base}/wp-json/wp/v2/product?page={page}&per_page={per_page}'
