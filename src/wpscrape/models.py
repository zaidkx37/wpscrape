"""Data models for wpscrape."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar

T = TypeVar('T')


@dataclass(frozen=True, slots=True)
class SiteInfo:
    """WordPress site metadata from /wp-json/."""

    name: str
    description: str
    url: str
    namespaces: list[str] = field(default_factory=list)
    has_woocommerce: bool = False

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'namespaces': self.namespaces,
            'has_woocommerce': self.has_woocommerce,
        }


@dataclass(frozen=True, slots=True)
class ProductImage:
    """A single product image."""

    id: int
    src: str
    thumbnail: str
    name: str
    alt: str

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'src': self.src,
            'thumbnail': self.thumbnail,
            'name': self.name,
            'alt': self.alt,
        }


@dataclass(frozen=True, slots=True)
class ProductPrice:
    """Pricing info for a product."""

    price: str
    regular_price: str
    sale_price: str
    currency_code: str
    currency_symbol: str
    currency_minor_unit: int = 0
    price_range: dict | None = None

    @property
    def price_float(self) -> float:
        """Price as a float, accounting for minor units."""
        try:
            raw = int(self.price)
            return raw / (10 ** self.currency_minor_unit) if self.currency_minor_unit else raw
        except (ValueError, TypeError):
            return 0.0

    @property
    def regular_price_float(self) -> float:
        """Regular price as a float."""
        try:
            raw = int(self.regular_price)
            return raw / (10 ** self.currency_minor_unit) if self.currency_minor_unit else raw
        except (ValueError, TypeError):
            return 0.0

    @property
    def sale_price_float(self) -> float:
        """Sale price as a float."""
        try:
            raw = int(self.sale_price)
            return raw / (10 ** self.currency_minor_unit) if self.currency_minor_unit else raw
        except (ValueError, TypeError):
            return 0.0

    @property
    def discount_percentage(self) -> float | None:
        """Calculate discount percentage from regular to sale price."""
        regular = self.regular_price_float
        sale = self.sale_price_float
        if regular > 0 and sale > 0 and sale < regular:
            return round((1 - sale / regular) * 100, 1)
        return None

    def to_dict(self) -> dict:
        result: dict = {
            'price': self.price_float,
            'regular_price': self.regular_price_float,
            'sale_price': self.sale_price_float,
            'currency_code': self.currency_code,
            'currency_symbol': self.currency_symbol,
        }
        discount = self.discount_percentage
        if discount is not None:
            result['discount_percentage'] = discount
        if self.price_range:
            result['price_range'] = self.price_range
        return result


@dataclass(frozen=True, slots=True)
class ProductCategory:
    """A category reference on a product."""

    id: int
    name: str
    slug: str
    link: str = ''

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'link': self.link,
        }


@dataclass(frozen=True, slots=True)
class ProductBrand:
    """A brand reference on a product."""

    id: int
    name: str
    slug: str
    link: str = ''

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'link': self.link,
        }


@dataclass(frozen=True, slots=True)
class ProductAttribute:
    """A product attribute (e.g. Size, Color)."""

    id: int
    name: str
    taxonomy: str
    has_variations: bool = False
    terms: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'taxonomy': self.taxonomy,
            'has_variations': self.has_variations,
            'terms': self.terms,
        }


@dataclass(frozen=True, slots=True)
class Product:
    """A WooCommerce product from the Store API."""

    id: int
    name: str
    slug: str
    permalink: str
    type: str
    sku: str
    short_description: str
    description: str
    on_sale: bool
    is_in_stock: bool
    is_on_backorder: bool
    average_rating: str
    review_count: int
    prices: ProductPrice | None = None
    categories: list[ProductCategory] = field(default_factory=list)
    brands: list[ProductBrand] = field(default_factory=list)
    images: list[ProductImage] = field(default_factory=list)
    attributes: list[ProductAttribute] = field(default_factory=list)
    variations: list[dict] = field(default_factory=list)
    has_options: bool = False
    low_stock_remaining: int | None = None
    parent: int = 0

    @property
    def url(self) -> str:
        """Product URL path."""
        return f'/product/{self.slug}'

    @property
    def price(self) -> float | None:
        """Current price as float."""
        if self.prices:
            return self.prices.price_float
        return None

    @property
    def regular_price(self) -> float | None:
        """Regular price as float."""
        if self.prices:
            return self.prices.regular_price_float
        return None

    @property
    def currency(self) -> str | None:
        """Currency code."""
        if self.prices:
            return self.prices.currency_code
        return None

    @property
    def primary_image(self) -> str | None:
        """URL of the first image."""
        if self.images:
            return self.images[0].src
        return None

    @property
    def category_names(self) -> list[str]:
        """List of category names."""
        return [c.name for c in self.categories]

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'permalink': self.permalink,
            'type': self.type,
            'sku': self.sku,
            'short_description': self.short_description,
            'on_sale': self.on_sale,
            'is_in_stock': self.is_in_stock,
            'is_on_backorder': self.is_on_backorder,
            'average_rating': self.average_rating,
            'review_count': self.review_count,
            'has_options': self.has_options,
            'low_stock_remaining': self.low_stock_remaining,
            'url': self.url,
            'price': self.price,
            'regular_price': self.regular_price,
            'currency': self.currency,
            'primary_image': self.primary_image,
            'category_names': self.category_names,
            'prices': self.prices.to_dict() if self.prices else None,
            'categories': [c.to_dict() for c in self.categories],
            'brands': [b.to_dict() for b in self.brands],
            'images': [i.to_dict() for i in self.images],
            'attributes': [a.to_dict() for a in self.attributes],
            'variations': self.variations,
        }

    def to_flat_dict(self) -> dict:
        """Flat dictionary for CSV export."""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'permalink': self.permalink,
            'type': self.type,
            'sku': self.sku,
            'price': self.price,
            'regular_price': self.regular_price,
            'currency': self.currency,
            'on_sale': self.on_sale,
            'is_in_stock': self.is_in_stock,
            'average_rating': self.average_rating,
            'review_count': self.review_count,
            'categories': ', '.join(self.category_names),
            'primary_image': self.primary_image,
            'image_count': len(self.images),
            'has_options': self.has_options,
        }


@dataclass(frozen=True, slots=True)
class Category:
    """A WooCommerce product category."""

    id: int
    name: str
    slug: str
    count: int
    parent: int
    description: str = ''
    image: dict | None = None

    @property
    def url(self) -> str:
        """Category URL path."""
        return f'/product-category/{self.slug}'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'count': self.count,
            'parent': self.parent,
            'description': self.description,
            'url': self.url,
            'image': self.image,
        }


@dataclass(frozen=True, slots=True)
class PaginatedResponse:
    """A paginated API response with metadata."""

    items: list
    page: int
    per_page: int
    total: int
    total_pages: int

    @property
    def has_next(self) -> bool:
        """True if there are more pages."""
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        """True if there is a previous page."""
        return self.page > 1

    def to_dict(self) -> dict:
        return {
            'items': [item.to_dict() for item in self.items],
            'page': self.page,
            'per_page': self.per_page,
            'total': self.total,
            'total_pages': self.total_pages,
            'has_next': self.has_next,
            'has_previous': self.has_previous,
        }
