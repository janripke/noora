import click

from .DropPlugin import DropPlugin


@click.command()
@click.option('-h', '--host', required=True, prompt=True, default='localhost')
@click.option('-d', '--database', required=False, prompt='Database name')
@click.option('-s', '--environment', required=False, prompt='Environment')
@click.option('-a', '--alias', required=False, prompt='Alias. Overrules the database option')
@click.pass_obj
def cli(props, host, database, environment, alias):
    """
    Drop a MySQL database.
    """
    plugin = DropPlugin()
    plugin.execute(
        props,
        {'host': host, 'database': database, 'environment': environment, 'alias': alias},
    )
