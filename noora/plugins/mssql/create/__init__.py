import click

from .CreatePlugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, prompt=True, default='localhost')
@click.option('-s', '--schema', required=False, prompt='Schema name')
@click.option('-s', '--environment', required=False, prompt='Environment')
@click.pass_obj
def cli(props, host, schema, environment):
    """
    Create a new MSSQL database.
    """
    plugin = CreatePlugin()
    plugin.execute(props, {'host': host, 'schema': schema, 'environment': environment})
