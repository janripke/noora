import click

from .CreatePlugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-s', '--schema', required=False, help='Schema name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.pass_obj
def cli(props, host, schema, environment):
    """
    Create a new MSSQL database.
    """
    plugin = CreatePlugin()
    plugin.execute(props, {'host': host, 'schema': schema, 'environment': environment})
