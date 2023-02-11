import click

from noora.plugins.postgresql.deploy.deploy_plugin import DeployPlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-v', '--version', required=False, help='The version to recreate')
@click.option('--connection-string', required=False)
@click.pass_obj
def cli(props, host, environment, version, connection_string):
    """
    Deploy a postgreSQL database.
    """
    plugin = DeployPlugin()
    plugin.execute(props, {'host': host, 'environment': environment, 'version': version,
                           'connection_string': connection_string})
