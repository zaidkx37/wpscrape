"""Quick usage example for wpscrape."""

from wpscrape import Exporter, WordPress

wp = WordPress('boskistores.com')

# Fetch site metadata
site = wp.site_info()
print(f'Site: {site.name}')
print(f'URL: {site.url}')
print(f'WooCommerce: {"Yes" if site.has_woocommerce else "No"}')
print()

# Fetch all categories
categories = wp.categories()
for c in categories:
    print(f'  {c.name} ({c.count} products)')

print(f'\n  ... {len(categories)} total categories\n')

# Fetch all products
products = wp.products()
for p in products[:5]:
    stock = 'In Stock' if p.is_in_stock else 'Out of Stock'
    price_str = f'{p.currency} {p.price:.0f}' if p.price else '-'
    print(f'  {p.name} - {price_str} ({stock})')

print(f'\n  ... {len(products)} total products\n')

# Export
exporter = Exporter()
exporter.products_to_json(products)
exporter.products_to_csv(products)
exporter.categories_to_json(categories)
exporter.site_to_json(site)
print('Exported to output/')
