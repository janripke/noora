import click

from .UpdatePlugin import UpdatePlugin


@click.command()
@click.option('-v', '--version', required=False)
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-s', '--schema', required=False, help='Schema name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.pass_obj
def cli(props, version, host, schema, environment):
    """
    Update an MSSQL database to the specified version.
    """
    plugin = UpdatePlugin()
    plugin.execute(
        props,
        {'version': version, 'host': host, 'schema': schema, 'environment': environment},
    )
