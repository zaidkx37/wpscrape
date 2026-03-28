from __future__ import annotations

from fastapi import APIRouter, Query

from wpscrape.api.deps import get_wordpress
from wpscrape.api.schemas import PaginatedProductsResponse, ProductResponse

router = APIRouter()


@router.get('/products', response_model=PaginatedProductsResponse | list[ProductResponse])
async def get_products(
    domain: str = Query(..., description='WooCommerce site domain'),
    category: str | None = Query(None, description='Filter by category slug'),
    search: str | None = Query(None, description='Search products by keyword'),
    page: int | None = Query(None, ge=1, description='Page number (omit to fetch all)'),
    per_page: int = Query(30, ge=1, le=100, description='Products per page (1-100)'),
) -> PaginatedProductsResponse | list[ProductResponse]:
    """Scrape products from a WordPress/WooCommerce store.

    Omit `page` to auto-paginate and fetch all products.
    Pass `page` to fetch a single page with pagination metadata.
    """
    wp = get_wordpress(domain)

    if page is not None:
        if search:
            result = wp.search_page(search, page=page, per_page=per_page)
        elif category:
            result = wp.category_products_page(category, page=page, per_page=per_page)
        else:
            result = wp.products_page(page=page, per_page=per_page)

        return PaginatedProductsResponse(
            items=[ProductResponse(**p.to_dict()) for p in result.items],
            page=result.page,
            per_page=result.per_page,
            total=result.total,
            total_pages=result.total_pages,
            has_next=result.has_next,
            has_previous=result.has_previous,
        )

    # Auto-paginate: return flat list
    if search:
        products = wp.search(search, per_page=per_page)
    elif category:
        products = wp.category_products(category)
    else:
        products = wp.products()

    return [ProductResponse(**p.to_dict()) for p in products]


@router.get('/products/{slug}', response_model=ProductResponse)
async def get_product(
    slug: str,
    domain: str = Query(..., description='WordPress/WooCommerce site domain'),
) -> ProductResponse:
    """Scrape a single product by slug."""
    wp = get_wordpress(domain)
    product = wp.product(slug)
    return ProductResponse(**product.to_dict())
