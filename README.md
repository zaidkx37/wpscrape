<div align="center">

# wpscrape

**Scrape any WordPress/WooCommerce store - products, categories & metadata from the public REST API.**

[![PyPI version](https://img.shields.io/pypi/v/wpscrape?color=blue)](https://pypi.org/project/wpscrape/)
[![Python](https://img.shields.io/pypi/pyversions/wpscrape)](https://pypi.org/project/wpscrape/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/zaidkx37/wpscrape/blob/main/LICENSE)
[![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen)]()

</div>

---

No API key or authentication required. Uses the public `wc/store/v1` endpoint designed for frontend access.

## Features

- **SDK** - Python client with full type hints and dataclass models
- **CLI** - Rich terminal output with tables, search, filtering, and export
- **REST API** - FastAPI server with auto-generated OpenAPI docs
- **Export** - JSON and CSV export out of the box
- **Pagination** - Auto-pagination or manual page-by-page control
- **Proxy support** - Route requests through any HTTP proxy
- **Retry logic** - Exponential backoff with jitter on transient failures

## Install

```bash
pip install wpscrape
```

With CLI support (rich tables):

```bash
pip install wpscrape[cli]
```

With REST API server:

```bash
pip install wpscrape[api]
```

Everything:

```bash
pip install wpscrape[all]
```

## Quick Start

### Python SDK

```python
from wpscrape import WordPress, Exporter

wp = WordPress("boskistores.com")

# Site metadata
site = wp.site_info()
print(site.name, site.has_woocommerce)

# All products (auto-paginates)
products = wp.products()
for p in products:
    print(p.name, p.price, p.currency)

# Search products
results = wp.search("smartwatch")

# Filter by category
earbuds = wp.category_products("earbuds")

# Single product by slug
product = wp.product("12v-router-power-bank")

# Paginated access
page = wp.products_page(page=1, per_page=10)
print(page.total, page.has_next)

# All categories
categories = wp.categories()

# Export to files
exporter = Exporter()
exporter.products_to_json(products)
exporter.products_to_csv(products)
exporter.categories_to_json(categories)
```

### CLI

```bash
# Scrape all products
wpscrape products boskistores.com

# Search products
wpscrape products boskistores.com --search smartwatch

# Filter by category
wpscrape products boskistores.com --category earbuds

# Paginated output
wpscrape products boskistores.com --page 1 --limit 10

# JSON output
wpscrape products boskistores.com --json

# Save to file
wpscrape products boskistores.com --save products.csv

# Categories
wpscrape categories boskistores.com

# Site info
wpscrape site boskistores.com

# Use a proxy
wpscrape --proxy http://user:pass@host:8080 products boskistores.com
```

### REST API

```bash
# Start the API server
wpscrape serve

# With custom host/port
wpscrape serve --host 0.0.0.0 --port 3000
```

Endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/products?domain=...` | List/search products |
| GET | `/api/v1/products/{slug}?domain=...` | Single product |
| GET | `/api/v1/categories?domain=...` | List categories |
| GET | `/api/v1/site?domain=...` | Site metadata |
| GET | `/health` | Health check |
| GET | `/docs` | OpenAPI docs |

## Configuration

### Proxy

```python
wp = WordPress("store.com", proxy="http://user:pass@host:8080")
```

Or via environment variable:

```bash
export WPSCRAPE_PROXY=http://user:pass@host:8080
wpscrape products store.com
```

### Timeout & Retries

```python
wp = WordPress("store.com", timeout=60.0, max_retries=5)
```

## Models

All data is returned as typed dataclasses:

- `SiteInfo` - site name, description, URL, namespaces, WooCommerce detection
- `Product` - full product data with prices, images, categories, attributes, variations
- `Category` - category with product count, parent, image
- `PaginatedResponse` - page metadata with `has_next` / `has_previous`

## License

[MIT](LICENSE)
