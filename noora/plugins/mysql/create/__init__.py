import click

from .CreatePlugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, prompt=True, default='localhost')
@click.option('-s', '--database', required=False, prompt='Database name')
@click.option('-s', '--environment', required=False, prompt='Environment')
@click.option('-a', '--alias', required=False, prompt='Alias. Overrules the database option')
@click.pass_obj
def cli(props, host, database, environment, alias):
    """
    Create a new MSSQL database.
    """
    plugin = CreatePlugin()
    plugin.execute(
        props,
        {'host': host, 'database': database, 'environment': environment, 'alias': alias},
    )
