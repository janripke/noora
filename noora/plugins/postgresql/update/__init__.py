import click

from noora.plugins.postgresql.update.UpdatePlugin import UpdatePlugin


@click.command()
@click.option('-v', '--version', required=False)
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-e', '--environment', required=False, help='Environment')
@click.pass_obj
def cli(props, version, host, environment):
    """
    Update a MSSQL database to the specified version.
    """
    plugin = UpdatePlugin()
    plugin.execute(props, {'version': version, 'host': host, 'environment': environment})
