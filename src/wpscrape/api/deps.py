from __future__ import annotations

from wpscrape.client import WordPress

_proxy: str | None = None


def set_proxy(proxy: str | None) -> None:
    """Set the global proxy for API-created WordPress instances."""
    global _proxy
    _proxy = proxy


def get_wordpress(domain: str) -> WordPress:
    """Create a WordPress client for the given domain."""
    return WordPress(domain, proxy=_proxy)
