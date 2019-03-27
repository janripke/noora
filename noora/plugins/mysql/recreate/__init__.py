import click

from .RecreatePlugin import RecreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-s', '--database', required=False, help='Database name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-a', '--alias', required=False, help='Alias. Overrules the database option')
@click.option('-v', '--version', required=False, help='The version to recreate')
@click.pass_obj
def cli(props, host, database, environment, alias, version):
    """
    Create a new MSSQL database.
    """
    plugin = RecreatePlugin()
    plugin.execute(
        props,
        {
            'host': host, 'database': database, 'environment': environment,
            'alias': alias, 'version': version
        },
    )
