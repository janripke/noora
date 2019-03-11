import click

from noora.connectors.MssqlConnector import MssqlConnector
from noora.plugins.mssql.generate.GeneratePlugin import GeneratePlugin


@click.command()
@click.option('-v', '--version', required=False, prompt=True)
@click.pass_obj
def cli(props, version):
    pass
    """
    Bootstrap a new version of a MSSQL database project
    """
    plugin = GeneratePlugin(props, MssqlConnector)
    plugin.prepare(version)
    plugin.execute()


@click.command()
@click.option('-h', '--host', required=False, prompt=True, default='localhost')
@click.option('-p', '--port', required=False, prompt=True, type=int, default=1433)
@click.option('-d', '--database', required=True, prompt='Database name')
@click.option('-s', '--schema', required=True, prompt='Schema name')
@click.option('-U', '--username', required=True, prompt='Database username')
@click.option('-P', '--password', required=True, prompt='Database password',
              hide_input=True, confirmation_prompt=True)
@click.option('-v', '--version', required=False,
              prompt='Initial project version', default='1.0.0')
@click.pass_obj
def cli_outside_scope(props, host, port, database, schema, username, password, version):
    """
    Generate a new MSSQL database project
    """
    plugin = GeneratePlugin(props, MssqlConnector)
    plugin.prepare(version, host, port, database, schema, username, password)
    plugin.execute()
