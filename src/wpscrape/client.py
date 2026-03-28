"""Main WordPress/WooCommerce client - public entry point for wpscrape."""

from __future__ import annotations

import logging

from wpscrape._endpoints import (
    api_index_url,
    categories_url,
    normalize_domain,
    product_by_slug_url,
    products_by_category_url,
    products_search_url,
    products_url,
)
from wpscrape._http import HTTPClient
from wpscrape._parsers import (
    parse_categories,
    parse_product,
    parse_products,
    parse_site_info,
)
from wpscrape.exceptions import (
    CategoryNotFoundError,
    ProductNotFoundError,
    RequestError,
    SiteNotFoundError,
)
from wpscrape.models import Category, PaginatedResponse, Product, SiteInfo

logger = logging.getLogger('wpscrape')


class WordPress:
    """Scrape any WordPress/WooCommerce store's public REST API.

    No API key or authentication required. Uses the ``wc/store/v1``
    namespace which is designed for public/frontend access.

    Args:
        domain: Site domain (e.g. ``'boskistores.com'``).
                Accepts with or without ``https://`` and ``www.`` prefix.
        proxy: Optional proxy URL (e.g. ``'http://user:pass@host:port'``).
        timeout: Request timeout in seconds.
        max_retries: Maximum retry attempts on transient failures.

    Examples::

        wp = WordPress('boskistores.com')
        products = wp.products()
        categories = wp.categories()

        # With proxy
        wp = WordPress('boskistores.com', proxy='http://user:pass@host:8080')
    """

    def __init__(
        self,
        domain: str,
        proxy: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._base = normalize_domain(domain)
        self._domain = domain
        self._http = HTTPClient(
            proxy=proxy,
            timeout=timeout,
            max_retries=max_retries,
        )

    def _get_json(self, url: str) -> dict | list:
        """Fetch a URL and return parsed JSON."""
        response = self._http.get(url)
        return response.json()

    def _get_response(self, url: str) -> tuple[dict | list, dict[str, str]]:
        """Fetch a URL and return parsed JSON + response headers."""
        response = self._http.get(url)
        return response.json(), dict(response.headers)

    @staticmethod
    def _extract_pagination(headers: dict[str, str], page: int, per_page: int) -> tuple[int, int]:
        """Extract total and total_pages from WP response headers."""
        total = int(headers.get('X-WP-Total', 0))
        total_pages = int(headers.get('X-WP-TotalPages', 0))
        return total, total_pages

    # ── Site Info ──

    def site_info(self) -> SiteInfo:
        """Fetch site metadata and check for WooCommerce.

        Returns:
            SiteInfo object with name, description, namespaces, etc.

        Raises:
            SiteNotFoundError: If the domain is not a WordPress site.
        """
        try:
            data = self._get_json(api_index_url(self._base))
        except RequestError:
            raise SiteNotFoundError(self._domain)
        return parse_site_info(data)

    # ── Products ──

    def products(self, per_page: int = 100) -> list[Product]:
        """Fetch all products from the store, auto-paginating.

        Args:
            per_page: Products per page (max 100). Pagination is automatic.

        Returns:
            List of all Product objects in the store.
        """
        all_products: list[Product] = []
        page = 1

        while True:
            url = products_url(self._base, page=page, per_page=per_page)
            data = self._get_json(url)
            if not isinstance(data, list):
                break
            batch = parse_products(data)
            if not batch:
                break
            all_products.extend(batch)
            if len(batch) < per_page:
                break
            page += 1

        logger.info('Fetched %d products from %s', len(all_products), self._domain)
        return all_products

    def products_page(self, page: int = 1, per_page: int = 30) -> PaginatedResponse:
        """Fetch a single page of products with pagination metadata.

        Args:
            page: Page number (1-indexed).
            per_page: Products per page (1-100).

        Returns:
            PaginatedResponse with products and pagination info
            (page, per_page, total, total_pages, has_next, has_previous).
        """
        url = products_url(self._base, page=page, per_page=per_page)
        data, headers = self._get_response(url)
        products = parse_products(data) if isinstance(data, list) else []
        total, total_pages = self._extract_pagination(headers, page, per_page)
        return PaginatedResponse(
            items=products, page=page, per_page=per_page,
            total=total, total_pages=total_pages,
        )

    def product(self, slug: str) -> Product:
        """Fetch a single product by slug.

        Args:
            slug: Product URL slug (e.g. ``'12v-router-power-bank'``).

        Returns:
            Product object.

        Raises:
            ProductNotFoundError: If the product slug doesn't exist.
        """
        try:
            data = self._get_json(product_by_slug_url(self._base, slug))
        except RequestError:
            raise ProductNotFoundError(slug)

        if isinstance(data, list):
            if not data:
                raise ProductNotFoundError(slug)
            return parse_product(data[0])
        return parse_product(data)

    def search(self, query: str, per_page: int = 100) -> list[Product]:
        """Search products by keyword, auto-paginating.

        Args:
            query: Search query string.
            per_page: Products per page (max 100).

        Returns:
            List of matching Product objects.
        """
        all_products: list[Product] = []
        page = 1

        while True:
            url = products_search_url(self._base, query, page=page, per_page=per_page)
            data = self._get_json(url)
            if not isinstance(data, list):
                break
            batch = parse_products(data)
            if not batch:
                break
            all_products.extend(batch)
            if len(batch) < per_page:
                break
            page += 1

        logger.info('Found %d products for query %r', len(all_products), query)
        return all_products

    def search_page(self, query: str, page: int = 1, per_page: int = 30) -> PaginatedResponse:
        """Search products by keyword with pagination metadata.

        Args:
            query: Search query string.
            page: Page number (1-indexed).
            per_page: Products per page (1-100).

        Returns:
            PaginatedResponse with products and pagination info.
        """
        url = products_search_url(self._base, query, page=page, per_page=per_page)
        data, headers = self._get_response(url)
        products = parse_products(data) if isinstance(data, list) else []
        total, total_pages = self._extract_pagination(headers, page, per_page)
        return PaginatedResponse(
            items=products, page=page, per_page=per_page,
            total=total, total_pages=total_pages,
        )

    # ── Categories ──

    def categories(self) -> list[Category]:
        """Fetch all product categories.

        Returns:
            List of Category objects.
        """
        data = self._get_json(categories_url(self._base))
        if not isinstance(data, list):
            return []
        result = parse_categories(data)
        logger.info('Fetched %d categories from %s', len(result), self._domain)
        return result

    def category_products(self, slug: str, per_page: int = 100) -> list[Product]:
        """Fetch all products in a specific category, auto-paginating.

        Args:
            slug: Category slug (e.g. ``'earbuds'``). Will be resolved to ID.
            per_page: Products per page (max 100).

        Returns:
            List of Product objects in the category.

        Raises:
            CategoryNotFoundError: If the category slug doesn't exist.
        """
        # Resolve slug to category ID
        cats = self.categories()
        cat = next((c for c in cats if c.slug == slug), None)
        if not cat:
            raise CategoryNotFoundError(slug)

        all_products: list[Product] = []
        page = 1

        while True:
            url = products_by_category_url(
                self._base, cat.id, page=page, per_page=per_page,
            )
            try:
                data = self._get_json(url)
            except RequestError:
                if page == 1:
                    raise CategoryNotFoundError(slug)
                break
            if not isinstance(data, list):
                break
            batch = parse_products(data)
            if not batch:
                break
            all_products.extend(batch)
            if len(batch) < per_page:
                break
            page += 1

        logger.info(
            'Fetched %d products from category %r', len(all_products), slug,
        )
        return all_products

    def category_products_page(
        self, slug: str, page: int = 1, per_page: int = 30,
    ) -> PaginatedResponse:
        """Fetch a single page of products from a category with pagination metadata.

        Args:
            slug: Category slug (e.g. ``'earbuds'``).
            page: Page number (1-indexed).
            per_page: Products per page (1-100).

        Returns:
            PaginatedResponse with products and pagination info.

        Raises:
            CategoryNotFoundError: If the category slug doesn't exist.
        """
        cats = self.categories()
        cat = next((c for c in cats if c.slug == slug), None)
        if not cat:
            raise CategoryNotFoundError(slug)

        url = products_by_category_url(
            self._base, cat.id, page=page, per_page=per_page,
        )
        try:
            data, headers = self._get_response(url)
        except RequestError:
            raise CategoryNotFoundError(slug)
        products = parse_products(data) if isinstance(data, list) else []
        total, total_pages = self._extract_pagination(headers, page, per_page)
        return PaginatedResponse(
            items=products, page=page, per_page=per_page,
            total=total, total_pages=total_pages,
        )

    def __repr__(self) -> str:
        return f'WordPress({self._domain!r})'
