from __future__ import annotations

from fastapi import APIRouter, Query

from wpscrape.api.deps import get_wordpress
from wpscrape.api.schemas import SiteInfoResponse

router = APIRouter()


@router.get('/site', response_model=SiteInfoResponse)
async def get_site_info(
    domain: str = Query(..., description='WooCommerce site domain'),
) -> SiteInfoResponse:
    """Fetch site metadata from a WordPress site."""
    wp = get_wordpress(domain)
    info = wp.site_info()
    return SiteInfoResponse(**info.to_dict())
