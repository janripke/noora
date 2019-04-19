import click

from noora.plugins.mssql.recreate.RecreatePlugin import RecreatePlugin


@click.command()
@click.option(
    '-h', '--host', required=True, default='localhost', help='The host to recreate the database on')
@click.option(
    '-e', '--environment', required=False, help='The environment to recreeate the database in')
@click.option('-v', '--version', required=False, help='The target version to recreate')
@click.pass_obj
def cli(props, host, environment, version):
    """
    Drop and recreate an MSSQL database to the specified or latest version.
    """
    plugin = RecreatePlugin()
    plugin.execute(
        props, {'host': host, 'environment': environment, 'version': version})
