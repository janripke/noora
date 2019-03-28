import click

from noora.plugins.mssql.create.CreatePlugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-s', '--schema', required=False, help='Schema name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.pass_obj
def cli(props, host, schema, environment):
    """
    Initialize an MSSQL database at the default version.
    """
    plugin = CreatePlugin()
    plugin.execute(props, {'host': host, 'schema': schema, 'environment': environment})
