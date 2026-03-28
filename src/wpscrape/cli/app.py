from __future__ import annotations

import click

from wpscrape import __version__


@click.group()
@click.version_option(version=__version__, prog_name='wpscrape')
@click.option('--proxy', envvar='WPSCRAPE_PROXY', default=None, help='HTTP proxy URL.')
@click.pass_context
def main(ctx: click.Context, proxy: str | None) -> None:
    """wpscrape - WordPress/WooCommerce store scraping toolkit.

    Scrape products, categories, and metadata from any WooCommerce store.
    No API key required.
    """
    ctx.ensure_object(dict)
    ctx.obj['proxy'] = proxy


def _register_commands() -> None:
    """Register CLI commands. Deferred to avoid import errors when extras not installed."""
    from wpscrape.cli.commands.categories import categories
    from wpscrape.cli.commands.products import products
    from wpscrape.cli.commands.site import site

    main.add_command(products)
    main.add_command(categories)
    main.add_command(site)

    try:
        from wpscrape.cli.commands.serve import serve
        main.add_command(serve)
    except ImportError:
        pass


_register_commands()


if __name__ == '__main__':
    main()
