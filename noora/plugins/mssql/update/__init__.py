import click

from noora.plugins.mssql.update.UpdatePlugin import UpdatePlugin


@click.command()
@click.option('-v', '--version', required=False, help='The version to update to')
@click.option(
    '-h', '--host', required=True, default='localhost', help='The host to update the db on')
@click.option('-e', '--environment', required=False, help='The environment to update the db in')
@click.pass_obj
def cli(props, version, host, environment):
    """
    Update an MSSQL database to the specified version.
    """
    plugin = UpdatePlugin()
    plugin.execute(props, {'version': version, 'host': host, 'environment': environment})
