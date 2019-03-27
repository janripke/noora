import click

from .RecreatePlugin import RecreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-s', '--schema', required=False, help='Schema name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-v', '--version', required=False, help='The version to recreate')
@click.pass_obj
def cli(props, host, schema, environment, version):
    """
    Create a new MSSQL database.
    """
    plugin = RecreatePlugin()
    plugin.execute(
        props, {'host': host, 'schema': schema, 'environment': environment, 'version': version})
