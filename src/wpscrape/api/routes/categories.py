from __future__ import annotations

from fastapi import APIRouter, Query

from wpscrape.api.deps import get_wordpress
from wpscrape.api.schemas import CategoryResponse

router = APIRouter()


@router.get('/categories', response_model=list[CategoryResponse])
async def get_categories(
    domain: str = Query(..., description='WordPress/WooCommerce site domain (e.g. boskistores.com)'),
) -> list[CategoryResponse]:
    """Scrape all product categories from a WooCommerce store."""
    wp = get_wordpress(domain)
    categories = wp.categories()
    return [CategoryResponse(**c.to_dict()) for c in categories]
