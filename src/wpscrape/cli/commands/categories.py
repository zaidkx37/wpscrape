from __future__ import annotations

import click

from wpscrape.cli.output import print_categories


@click.command()
@click.argument('domain')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON.')
@click.option('--save', '-s', default=None, help='Save to JSON file.')
@click.pass_context
def categories(
    ctx: click.Context,
    domain: str,
    output_json: bool,
    save: str | None,
) -> None:
    """Scrape product categories from a WooCommerce store.

    \b
    Examples:
        wpscrape categories boskistores.com
        wpscrape categories boskistores.com --json
        wpscrape categories boskistores.com --save categories.json
    """
    from wpscrape import Exporter, WordPress

    proxy = ctx.obj.get('proxy')
    wp = WordPress(domain, proxy=proxy)
    result = wp.categories()

    if save:
        exporter = Exporter()
        exporter.categories_to_json(result, filename=save)
        click.echo(f'Saved {len(result)} categories to output/{save}')
    else:
        print_categories(result, output_json=output_json)
