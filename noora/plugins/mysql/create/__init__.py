import click

from noora.plugins.mysql.create.CreatePlugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-d', '--database', required=False, help='Database name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-a', '--alias', required=False, help='Alias. Overrules the database option')
@click.pass_obj
def cli(props, host, database, environment, alias):
    """
    Initialize a MySQL database at the default version.
    """
    plugin = CreatePlugin()
    plugin.execute(
        props,
        {'host': host, 'database': database, 'environment': environment, 'alias': alias},
    )
