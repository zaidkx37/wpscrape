from __future__ import annotations

import click

from wpscrape.cli.output import print_paginated_products, print_products


@click.command()
@click.argument('domain')
@click.option('--category', '-c', default=None, help='Filter by category slug.')
@click.option('--search', '-q', default=None, help='Search products by keyword.')
@click.option('--page', '-p', default=None, type=int, help='Page number (manual pagination).')
@click.option('--limit', '-l', default=30, type=int, help='Products per page (1-100, default 30).')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON.')
@click.option('--save', '-s', default=None, help='Save to file (json or csv).')
@click.pass_context
def products(
    ctx: click.Context,
    domain: str,
    category: str | None,
    search: str | None,
    page: int | None,
    limit: int,
    output_json: bool,
    save: str | None,
) -> None:
    """Scrape products from a WordPress/WooCommerce store.

    \b
    Examples:
        wpscrape products boskistores.com
        wpscrape products boskistores.com --category earbuds
        wpscrape products boskistores.com --search smartwatch
        wpscrape products boskistores.com --page 1 --limit 10
        wpscrape products boskistores.com --json
        wpscrape products boskistores.com --save products.csv
    """
    from wpscrape import Exporter, WordPress

    proxy = ctx.obj.get('proxy')
    wp = WordPress(domain, proxy=proxy)

    if page is not None:
        # Paginated mode - returns PaginatedResponse
        if search:
            result = wp.search_page(search, page=page, per_page=limit)
        elif category:
            result = wp.category_products_page(category, page=page, per_page=limit)
        else:
            result = wp.products_page(page=page, per_page=limit)

        if save:
            exporter = Exporter()
            if save.endswith('.csv'):
                exporter.products_to_csv(result.items, filename=save)
            else:
                exporter.products_to_json(result.items, filename=save)
            click.echo(f'Saved {len(result.items)} products to output/{save}')
        else:
            print_paginated_products(result, output_json=output_json)
    else:
        # Auto-paginate mode - returns list[Product]
        if search:
            items = wp.search(search, per_page=limit)
        elif category:
            items = wp.category_products(category)
        else:
            items = wp.products()

        if save:
            exporter = Exporter()
            if save.endswith('.csv'):
                exporter.products_to_csv(items, filename=save)
            else:
                exporter.products_to_json(items, filename=save)
            click.echo(f'Saved {len(items)} products to output/{save}')
        else:
            print_products(items, output_json=output_json)
