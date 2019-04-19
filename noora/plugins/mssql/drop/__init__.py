import click

from noora.plugins.mssql.drop.DropPlugin import DropPlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost', help='The host to drop the database on')
@click.option('-e', '--environment', required=False, help='The environment to drop the database in')
@click.pass_obj
def cli(props, host, environment):
    """
    Drop (empty) an MSSQL database.
    """
    plugin = DropPlugin()
    plugin.execute(props, {'host': host, 'environment': environment})
