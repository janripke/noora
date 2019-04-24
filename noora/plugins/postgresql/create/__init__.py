import click

from noora.plugins.postgresql.create.CreatePlugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-e', '--environment', required=False, help='Environment')
@click.pass_obj
def cli(props, host, environment):
    """
    Initialize a PostgreSQL database at the default version.
    """
    plugin = CreatePlugin()
    plugin.execute(props, {'host': host, 'environment': environment})
