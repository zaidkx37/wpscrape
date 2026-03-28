from __future__ import annotations

import click

from wpscrape.cli.output import print_site_info


@click.command()
@click.argument('domain')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON.')
@click.option('--save', '-s', default=None, help='Save to JSON file.')
@click.pass_context
def site(
    ctx: click.Context,
    domain: str,
    output_json: bool,
    save: str | None,
) -> None:
    """Fetch site metadata from a WordPress site.

    \b
    Examples:
        wpscrape site boskistores.com
        wpscrape site boskistores.com --json
        wpscrape site boskistores.com --save site.json
    """
    from wpscrape import Exporter, WordPress

    proxy = ctx.obj.get('proxy')
    wp = WordPress(domain, proxy=proxy)
    result = wp.site_info()

    if save:
        exporter = Exporter()
        exporter.site_to_json(result, filename=save)
        click.echo(f'Saved site metadata to output/{save}')
    else:
        print_site_info(result, output_json=output_json)
