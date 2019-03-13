import click

from .UpdatePlugin import UpdatePlugin


@click.command()
@click.option('-v', '--version', required=False)
@click.option('-h', '--host', required=True, prompt=True, default='localhost')
@click.option('-s', '--database', required=False, prompt='Database name')
@click.option('-s', '--environment', required=False, prompt='Environment')
@click.option('-a', '--alias', required=False, prompt='Alias. Overrules the database option')
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
