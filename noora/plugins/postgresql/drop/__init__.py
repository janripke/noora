import click

from noora.plugins.postgresql.drop.DropPlugin import DropPlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-e', '--environment', required=False, help='Environment')
@click.pass_obj
def cli(props, host, environment):
    """
    Drop (empty) a PostgreSQL database.
    """
    plugin = DropPlugin()
    plugin.execute(props, {'host': host, 'environment': environment})
