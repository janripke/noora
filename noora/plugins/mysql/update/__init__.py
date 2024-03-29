import click

from noora.plugins.mysql.update.update_plugin import UpdatePlugin


@click.command()
@click.option('-v', '--version', required=False)
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-d', '--database', required=False, help='Database name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-a', '--alias', required=False, help='Alias. Overrules the database option')
@click.option('--connection-string', required=False)
@click.pass_obj
def cli(props, version, host, database, environment, alias, connection_string):
    """
    Update a MSSQL database to the specified version.
    """
    plugin = UpdatePlugin()
    plugin.execute(
        props,
        {
            'version': version, 'host': host, 'database': database,
            'environment': environment, 'alias': alias, 'connection_string': connection_string
        },
    )
