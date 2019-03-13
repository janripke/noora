import click

from .BuildPlugin import BuildPlugin


@click.command()
@click.option('-v', '--version', required=True)
@click.option('-d', '--database', required=False)
@click.pass_obj
def cli(props, version, database):
    pass
    """
    Bootstrap a new version of a MySQL database project
    """
    plugin = BuildPlugin()
    plugin.execute(props, {'version': version, 'database': database})
