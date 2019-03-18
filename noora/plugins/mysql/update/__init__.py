import click

from .UpdatePlugin import UpdatePlugin


@click.command()
@click.option('-v', '--version', required=False)
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-s', '--database', required=False, help='Database name')
@click.option('-s', '--environment', required=False, help='Environment')
@click.option('-a', '--alias', required=False, help='Alias. Overrules the database option')
@click.pass_obj
def cli(props, version, host, database, environment, alias):
    """
    Update a MySQL database.
    """
    plugin = UpdatePlugin()
    plugin.execute(
        props,
        {
            'version': version, 'host': host, 'database': database,
            'environment': environment, 'alias': alias
        },
    )
