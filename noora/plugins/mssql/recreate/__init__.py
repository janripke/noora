import click

from noora.connectors.MssqlConnector import MssqlConnector
from .RecreatePlugin import RecreatePlugin


@click.command()
@click.option('-h', '--host', required=True, prompt=True, default='localhost')
@click.option('-s', '--schema', required=False, prompt='Schema name')
@click.option('-s', '--environment', required=False, prompt='Environment')
@click.pass_obj
def cli(props, host, schema, environment):
    """
    Create a new MSSQL database.
    """
    plugin = RecreatePlugin(props, MssqlConnector)
    plugin.prepare(host, schema, environment)
    plugin.execute()
