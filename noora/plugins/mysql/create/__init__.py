import click

from noora.plugins.mysql.create.create_plugin import CreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-d', '--database', required=False, help='Database name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-a', '--alias', required=False, help='Alias. Overrules the database option')
@click.option('--connection-string', required=False)
@click.pass_obj
def cli(props, host, database, environment, alias, connection_string):
    """
    Initialize a MySQL database at the default version.
    """
    plugin = CreatePlugin()
    plugin.execute(
        props,
        {'host': host, 'database': database, 'environment': environment, 'alias': alias, 'connection_string': connection_string},
    )
