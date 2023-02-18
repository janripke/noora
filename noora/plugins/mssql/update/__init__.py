import click

from noora.plugins.mssql.update.update_plugin import UpdatePlugin


@click.command()
@click.option('-v', '--version', required=False, help='The version to update to')
@click.option('-h', '--host', required=True, default='localhost', help='The host to update the db on')
@click.option('-e', '--environment', required=False, help='The environment to update the db in')
@click.option('--connection-string', required=False)
@click.pass_obj
def cli(props, version, host, environment, connection_string):
    """
    Update an MSSQL database to the specified version.
    """
    plugin = UpdatePlugin()
    plugin.execute(props, {'version': version, 'host': host, 'environment': environment,
                           'connection_string': connection_string})
