from __future__ import annotations

from pydantic import BaseModel


class ProductPriceResponse(BaseModel):
    price: float
    regular_price: float
    sale_price: float
    currency_code: str
    currency_symbol: str
    discount_percentage: float | None = None
    price_range: dict | None = None


class ProductImageResponse(BaseModel):
    id: int
    src: str
    thumbnail: str
    name: str
    alt: str


class ProductCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    link: str = ''


class ProductBrandResponse(BaseModel):
    id: int
    name: str
    slug: str
    link: str = ''


class ProductAttributeResponse(BaseModel):
    id: int
    name: str
    taxonomy: str
    has_variations: bool = False
    terms: list[dict] = []


class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    permalink: str
    type: str
    sku: str
    short_description: str
    on_sale: bool
    is_in_stock: bool
    is_on_backorder: bool
    average_rating: str
    review_count: int
    has_options: bool
    low_stock_remaining: int | None
    url: str
    price: float | None
    regular_price: float | None
    currency: str | None
    primary_image: str | None
    category_names: list[str]
    prices: ProductPriceResponse | None = None
    categories: list[ProductCategoryResponse] = []
    brands: list[ProductBrandResponse] = []
    images: list[ProductImageResponse] = []
    attributes: list[ProductAttributeResponse] = []
    variations: list[dict] = []


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    count: int
    parent: int
    description: str
    url: str
    image: dict | None = None


class SiteInfoResponse(BaseModel):
    name: str
    description: str
    url: str
    namespaces: list[str]
    has_woocommerce: bool


class PaginatedProductsResponse(BaseModel):
    items: list[ProductResponse]
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None


class HealthResponse(BaseModel):
    status: str = 'ok'
    version: str
