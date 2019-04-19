import click

from noora.plugins.mssql.create.CreatePlugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost', help='The host to deploy to')
@click.option('-e', '--environment', required=False, help='The environment to deploy in')
@click.pass_obj
def cli(props, host, environment):
    """
    Initialize an MSSQL database at the default version.
    """
    plugin = CreatePlugin()
    plugin.execute(props, {'host': host, 'environment': environment})
