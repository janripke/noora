import click

from noora.plugins.postgresql.create.CreatePlugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('--connection-string', required=False)
@click.pass_obj
def cli(props, host, environment, connection_string):
    """
    Initialize a PostgreSQL database at the default version.
    """
    plugin = CreatePlugin()
    plugin.execute(props, {'host': host, 'environment': environment, 'connection_string': connection_string})
