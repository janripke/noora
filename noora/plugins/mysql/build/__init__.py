import click

from .BuildPlugin import BuildPlugin


@click.command()
@click.option('-v', '--version', required=True)
@click.option('-d', '--database', required=False)
@click.pass_obj
def cli(props, version, database):
    """
    Build a package for this MySQL database.
    """
    plugin = BuildPlugin()
    plugin.execute(props, {'version': version, 'database': database})
