from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from wpscrape import __version__
from wpscrape.api.deps import set_proxy
from wpscrape.api.routes import categories, products, site
from wpscrape.api.schemas import ErrorResponse, HealthResponse
from wpscrape.exceptions import (
    CategoryNotFoundError,
    ProductNotFoundError,
    RateLimitError,
    RequestError,
    SiteNotFoundError,
    WPScrapeError,
)


def create_app(
    proxy: str | None = None,
    title: str = 'WPScrape API',
) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        proxy: Optional proxy URL for requests.
        title: API title shown in docs.

    Returns:
        Configured FastAPI application.
    """
    app = FastAPI(
        title=title,
        version=__version__,
        description='WordPress/WooCommerce store scraping API: products, categories & metadata.',
    )

    if proxy:
        set_proxy(proxy)

    # Routes
    app.include_router(products.router, prefix='/api/v1', tags=['products'])
    app.include_router(categories.router, prefix='/api/v1', tags=['categories'])
    app.include_router(site.router, prefix='/api/v1', tags=['site'])

    # Health check
    @app.get('/health', response_model=HealthResponse, tags=['health'])
    async def health():
        return HealthResponse(version=__version__)

    # Exception handlers
    @app.exception_handler(SiteNotFoundError)
    async def site_not_found_handler(request: Request, exc: SiteNotFoundError):
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(error='site_not_found', detail=str(exc)).model_dump(),
        )

    @app.exception_handler(ProductNotFoundError)
    async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(error='product_not_found', detail=str(exc)).model_dump(),
        )

    @app.exception_handler(CategoryNotFoundError)
    async def category_not_found_handler(request: Request, exc: CategoryNotFoundError):
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(error='category_not_found', detail=str(exc)).model_dump(),
        )

    @app.exception_handler(RateLimitError)
    async def rate_limit_handler(request: Request, exc: RateLimitError):
        return JSONResponse(
            status_code=429,
            content=ErrorResponse(error='rate_limited', detail=str(exc)).model_dump(),
        )

    @app.exception_handler(RequestError)
    async def request_error_handler(request: Request, exc: RequestError):
        return JSONResponse(
            status_code=502,
            content=ErrorResponse(error='upstream_error', detail=str(exc)).model_dump(),
        )

    @app.exception_handler(WPScrapeError)
    async def wpscrape_error_handler(request: Request, exc: WPScrapeError):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(error='wpscrape_error', detail=str(exc)).model_dump(),
        )

    return app
