from __future__ import annotations

import json
import sys

from wpscrape.models import Category, PaginatedResponse, Product, SiteInfo


def _safe_str(text: str | None) -> str:
    """Replace characters that can't be encoded in the current terminal."""
    if not text:
        return ''
    try:
        text.encode(sys.stdout.encoding or 'utf-8')
        return text
    except (UnicodeEncodeError, LookupError):
        return text.encode('ascii', errors='replace').decode('ascii')


def _json_print(data: object) -> None:
    """Print JSON, handling encoding issues on Windows."""
    text = json.dumps(data, indent=2, ensure_ascii=False)
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(text.encode('utf-8'))
        sys.stdout.buffer.write(b'\n')


def print_products(products: list[Product], output_json: bool = False) -> None:
    """Print products to terminal."""
    if output_json:
        _json_print([p.to_dict() for p in products])
        return

    try:
        from rich.console import Console
        from rich.table import Table

        console = Console(force_terminal=True)
        table = Table(title='Products', show_lines=True)
        table.add_column('#', style='dim', width=4)
        table.add_column('Name', style='bold', max_width=45)
        table.add_column('Price', justify='right', style='green')
        table.add_column('Regular', justify='right', style='dim')
        table.add_column('Stock', justify='center')
        table.add_column('Rating', justify='center', style='yellow')

        for i, product in enumerate(products, start=1):
            stock = '[green]Yes[/green]' if product.is_in_stock else '[red]No[/red]'
            price_str = f'{product.price:.0f}' if product.price else '-'
            regular_str = f'{product.regular_price:.0f}' if product.regular_price else '-'
            rating = product.average_rating if product.average_rating != '0' else '-'
            sale = ' [red]SALE[/red]' if product.on_sale else ''
            table.add_row(
                str(i),
                _safe_str(product.name) + sale,
                price_str,
                regular_str,
                stock,
                rating,
            )

        console.print(table)
        console.print(f'[dim]{len(products)} products[/dim]')

    except ImportError:
        _print_products_plain(products)


def _pagination_footer(result: PaginatedResponse) -> str:
    """Build pagination info string."""
    return (
        f'Page {result.page}/{result.total_pages} '
        f'({len(result.items)} items, {result.total} total)'
    )


def print_paginated_products(result: PaginatedResponse, output_json: bool = False) -> None:
    """Print paginated products with pagination metadata."""
    if output_json:
        _json_print(result.to_dict())
        return

    try:
        from rich.console import Console
        from rich.table import Table

        console = Console(force_terminal=True)
        title = f'Products - Page {result.page}/{result.total_pages} ({result.total} total)'
        table = Table(title=title, show_lines=True)
        table.add_column('#', style='dim', width=4)
        table.add_column('Name', style='bold', max_width=45)
        table.add_column('Price', justify='right', style='green')
        table.add_column('Regular', justify='right', style='dim')
        table.add_column('Stock', justify='center')
        table.add_column('Rating', justify='center', style='yellow')

        for i, product in enumerate(result.items, start=1):
            stock = '[green]Yes[/green]' if product.is_in_stock else '[red]No[/red]'
            price_str = f'{product.price:.0f}' if product.price else '-'
            regular_str = f'{product.regular_price:.0f}' if product.regular_price else '-'
            rating = product.average_rating if product.average_rating != '0' else '-'
            sale = ' [red]SALE[/red]' if product.on_sale else ''
            table.add_row(
                str(i),
                _safe_str(product.name) + sale,
                price_str,
                regular_str,
                stock,
                rating,
            )

        console.print(table)
        footer = _pagination_footer(result)
        if result.has_next:
            footer += f'  [cyan]Next: --page {result.page + 1}[/cyan]'
        console.print(f'[dim]{footer}[/dim]')

    except ImportError:
        _print_products_plain(result.items)
        print(_pagination_footer(result))


def print_categories(categories: list[Category], output_json: bool = False) -> None:
    """Print categories to terminal."""
    if output_json:
        _json_print([c.to_dict() for c in categories])
        return

    try:
        from rich.console import Console
        from rich.table import Table

        console = Console(force_terminal=True)
        table = Table(title='Categories', show_lines=True)
        table.add_column('#', style='dim', width=4)
        table.add_column('Name', style='bold', max_width=40)
        table.add_column('Slug', style='cyan', max_width=30)
        table.add_column('Products', justify='right')

        for i, cat in enumerate(categories, start=1):
            table.add_row(
                str(i),
                _safe_str(cat.name),
                _safe_str(cat.slug),
                str(cat.count),
            )

        console.print(table)
        console.print(f'[dim]{len(categories)} categories[/dim]')

    except ImportError:
        _print_categories_plain(categories)


def print_site_info(site: SiteInfo, output_json: bool = False) -> None:
    """Print site metadata to terminal."""
    if output_json:
        _json_print(site.to_dict())
        return

    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table

        console = Console(force_terminal=True)
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column('Key', style='bold')
        table.add_column('Value')
        table.add_row('Name', site.name)
        table.add_row('Description', site.description)
        table.add_row('URL', site.url)
        woo = '[green]Yes[/green]' if site.has_woocommerce else '[red]No[/red]'
        table.add_row('WooCommerce', woo)
        table.add_row('Namespaces', ', '.join(site.namespaces[:10]))

        console.print(Panel(table, title=site.name, border_style='cyan'))

    except ImportError:
        _print_site_info_plain(site)


def _print_products_plain(products: list[Product]) -> None:
    """Fallback plain text output for products."""
    print('Products\n')
    for i, p in enumerate(products, start=1):
        stock = 'In Stock' if p.is_in_stock else 'Out of Stock'
        price_str = f'{p.price:.0f}' if p.price else '-'
        print(f'{i}. {p.name}')
        print(f'   Price: {price_str} | {stock}')
        print()


def _print_categories_plain(categories: list[Category]) -> None:
    """Fallback plain text output for categories."""
    print('Categories\n')
    for i, c in enumerate(categories, start=1):
        print(f'{i}. {c.name} ({c.slug}) - {c.count} products')


def _print_site_info_plain(site: SiteInfo) -> None:
    """Fallback plain text output for site info."""
    print(f'Site: {site.name}')
    print(f'URL: {site.url}')
    print(f'Description: {site.description}')
    print(f'WooCommerce: {"Yes" if site.has_woocommerce else "No"}')
