import click

from noora.plugins.mysql.update.UpdatePlugin import UpdatePlugin


@click.command()
@click.option('-v', '--version', required=False)
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-d', '--database', required=False, help='Database name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-a', '--alias', required=False, help='Alias. Overrules the database option')
@click.pass_obj
def cli(props, version, host, database, environment, alias):
    """
    Update a MSSQL database to the specified version.
    """
    plugin = UpdatePlugin()
    plugin.execute(
        props,
        {
            'version': version, 'host': host, 'database': database,
            'environment': environment, 'alias': alias
        },
    )
