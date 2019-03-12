import click

from noora.connectors.MssqlConnector import MssqlConnector
from .UpdatePlugin import UpdatePlugin


@click.command()
@click.option('-v', '--version', required=False)
@click.option('-h', '--host', required=True, prompt=True, default='localhost')
@click.option('-s', '--schema', required=False, prompt='Schema name')
@click.option('-s', '--environment', required=False, prompt='Environment')
@click.pass_obj
def cli(props, version, host, schema, environment):
    """
    Create a new MSSQL database.
    """
    plugin = UpdatePlugin(props, MssqlConnector)
    plugin.prepare(version, host, schema, environment)
    plugin.execute()
