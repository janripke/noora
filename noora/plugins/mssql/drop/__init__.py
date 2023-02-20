import click

from noora.plugins.mssql.drop.drop_plugin import DropPlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost', help='The host to drop the database on')
@click.option('-e', '--environment', required=False, help='The environment to drop the database in')
@click.option('--connection-string', required=False)
@click.pass_obj
def cli(props, host, environment, connection_string):
    """
    Drop (empty) an MSSQL database.
    """
    plugin = DropPlugin()
    plugin.execute(props, {'host': host, 'environment': environment, 'connection_string': connection_string})
