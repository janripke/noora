import click

from noora.plugins.postgresql.create.CreatePlugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-s', '--database', required=False, help='Database name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-a', '--alias', required=False, help='Alias. Overrules the database option')
@click.pass_obj
def cli(props, host, database, environment, alias):
    """
    Initialize a PostgreSQL database at the default version.
    """
    plugin = CreatePlugin()
    plugin.execute(
        props,
        {'host': host, 'database': database, 'environment': environment, 'alias': alias},
    )
