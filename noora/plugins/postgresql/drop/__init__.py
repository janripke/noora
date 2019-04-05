import click

from noora.plugins.postgresql.drop.DropPlugin import DropPlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-d', '--database', required=False, help='Database name')
@click.option('-s', '--environment', required=False, help='Environment')
@click.option('-a', '--alias', required=False, help='Alias. Overrules the database option')
@click.pass_obj
def cli(props, host, database, environment, alias):
    """
    Drop (empty) a PostgreSQL database.
    """
    plugin = DropPlugin()
    plugin.execute(
        props,
        {'host': host, 'database': database, 'environment': environment, 'alias': alias},
    )