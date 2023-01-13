import click

from noora.plugins.postgresql.recreate.RecreatePlugin import RecreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-v', '--version', required=False, help='The version to recreate')
@click.option('--connection-string', required=False)
@click.pass_obj
def cli(props, host, environment, version, connection_string):
    """
    Drop and recreate a PostgreSQL database to the specified or latest version.
    """
    plugin = RecreatePlugin()
    plugin.execute(props, {'host': host, 'environment': environment, 'version': version,
                           'connection_string': connection_string})
