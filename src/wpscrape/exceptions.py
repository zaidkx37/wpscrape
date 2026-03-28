"""Exception hierarchy for wpscrape."""

from __future__ import annotations


class WPScrapeError(Exception):
    """Base exception for all wpscrape errors."""


class SiteNotFoundError(WPScrapeError):
    """Site does not exist or is not a WordPress/WooCommerce site."""

    def __init__(self, domain: str) -> None:
        self.domain = domain
        super().__init__(f"Site not found or not a WordPress/WooCommerce site: '{domain}'")


class ProductNotFoundError(WPScrapeError):
    """Product slug does not exist."""

    def __init__(self, slug: str) -> None:
        self.slug = slug
        super().__init__(f"Product not found: '{slug}'")


class CategoryNotFoundError(WPScrapeError):
    """Category slug does not exist."""

    def __init__(self, slug: str) -> None:
        self.slug = slug
        super().__init__(f"Category not found: '{slug}'")


class RateLimitError(WPScrapeError):
    """Site rate limit hit (HTTP 429)."""

    def __init__(self, message: str = 'Rate limited by WordPress') -> None:
        super().__init__(message)


class RequestError(WPScrapeError):
    """HTTP request failed."""

    def __init__(self, status_code: int, message: str = '') -> None:
        self.status_code = status_code
        super().__init__(f'HTTP {status_code}: {message}' if message else f'HTTP {status_code}')


class ParsingError(WPScrapeError):
    """Failed to parse site response."""
