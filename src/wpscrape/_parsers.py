"""Response parsers - JSON dicts to dataclass models."""

from __future__ import annotations

from wpscrape.models import (
    Category,
    Product,
    ProductAttribute,
    ProductBrand,
    ProductCategory,
    ProductImage,
    ProductPrice,
    SiteInfo,
)


def parse_site_info(data: dict) -> SiteInfo:
    """Parse /wp-json/ response into a SiteInfo model."""
    namespaces = data.get('namespaces', [])
    has_woocommerce = any(ns.startswith('wc/') for ns in namespaces)
    return SiteInfo(
        name=data.get('name', ''),
        description=data.get('description', ''),
        url=data.get('url', ''),
        namespaces=namespaces,
        has_woocommerce=has_woocommerce,
    )


def parse_image(data: dict) -> ProductImage:
    """Parse a single product image dict."""
    return ProductImage(
        id=data.get('id', 0),
        src=data.get('src', ''),
        thumbnail=data.get('thumbnail', ''),
        name=data.get('name', ''),
        alt=data.get('alt', ''),
    )


def parse_price(data: dict) -> ProductPrice:
    """Parse a prices object from the Store API."""
    return ProductPrice(
        price=data.get('price', '0'),
        regular_price=data.get('regular_price', '0'),
        sale_price=data.get('sale_price', '0'),
        currency_code=data.get('currency_code', ''),
        currency_symbol=data.get('currency_symbol', ''),
        currency_minor_unit=data.get('currency_minor_unit', 0),
        price_range=data.get('price_range'),
    )


def parse_product_category(data: dict) -> ProductCategory:
    """Parse a category reference on a product."""
    return ProductCategory(
        id=data.get('id', 0),
        name=data.get('name', ''),
        slug=data.get('slug', ''),
        link=data.get('link', ''),
    )


def parse_product_brand(data: dict) -> ProductBrand:
    """Parse a brand reference on a product."""
    return ProductBrand(
        id=data.get('id', 0),
        name=data.get('name', ''),
        slug=data.get('slug', ''),
        link=data.get('link', ''),
    )


def parse_attribute(data: dict) -> ProductAttribute:
    """Parse a product attribute dict."""
    return ProductAttribute(
        id=data.get('id', 0),
        name=data.get('name', ''),
        taxonomy=data.get('taxonomy', ''),
        has_variations=data.get('has_variations', False),
        terms=data.get('terms', []),
    )


def parse_product(data: dict) -> Product:
    """Parse a single product dict from the WC Store API."""
    prices_data = data.get('prices')
    return Product(
        id=data.get('id', 0),
        name=data.get('name', ''),
        slug=data.get('slug', ''),
        permalink=data.get('permalink', ''),
        type=data.get('type', 'simple'),
        sku=data.get('sku', ''),
        short_description=data.get('short_description', ''),
        description=data.get('description', ''),
        on_sale=data.get('on_sale', False),
        is_in_stock=data.get('is_in_stock', False),
        is_on_backorder=data.get('is_on_backorder', False),
        average_rating=data.get('average_rating', '0'),
        review_count=data.get('review_count', 0),
        prices=parse_price(prices_data) if prices_data else None,
        categories=[parse_product_category(c) for c in data.get('categories', [])],
        brands=[parse_product_brand(b) for b in data.get('brands', [])],
        images=[parse_image(i) for i in data.get('images', [])],
        attributes=[parse_attribute(a) for a in data.get('attributes', [])],
        variations=data.get('variations', []),
        has_options=data.get('has_options', False),
        low_stock_remaining=data.get('low_stock_remaining'),
        parent=data.get('parent', 0),
    )


def parse_products(data: list) -> list[Product]:
    """Parse Store API products response (JSON array)."""
    return [parse_product(p) for p in data]


def parse_category(data: dict) -> Category:
    """Parse a single category dict."""
    return Category(
        id=data.get('id', 0),
        name=data.get('name', ''),
        slug=data.get('slug', ''),
        count=data.get('count', 0),
        parent=data.get('parent', 0),
        description=data.get('description', ''),
        image=data.get('image'),
    )


def parse_categories(data: list) -> list[Category]:
    """Parse Store API categories response (JSON array)."""
    return [parse_category(c) for c in data]
