import click

from noora.plugins.mssql.create.create_plugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost', help='The host to deploy to')
@click.option('-e', '--environment', required=False, help='The environment to deploy in')
@click.option('--connection-string', required=False)
@click.pass_obj
def cli(props, host, environment, connection_string):
    """
    Initialize an MSSQL database at the default version.
    """
    plugin = CreatePlugin()
    plugin.execute(props, {'host': host, 'environment': environment, 'connection_string': connection_string})
