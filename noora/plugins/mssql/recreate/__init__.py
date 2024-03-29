import click

from noora.plugins.mssql.recreate.recreate_plugin import RecreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost', help='The host to recreate the database on')
@click.option('-e', '--environment', required=False, help='The environment to recreeate the database in')
@click.option('-v', '--version', required=False, help='The target version to recreate')
@click.option('--connection-string', required=False)
@click.pass_obj
def cli(props, host, environment, version, connection_string):
    """
    Drop and recreate an MSSQL database to the specified or latest version.
    """
    plugin = RecreatePlugin()
    plugin.execute(
        props, {'host': host, 'environment': environment, 'version': version, 'connection_string': connection_string})
