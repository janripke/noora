import click

from noora.plugins.mysql.recreate.RecreatePlugin import RecreatePlugin


@click.command()
@click.option('-h', '--host', required=True, default='localhost')
@click.option('-d', '--database', required=False, help='Database name')
@click.option('-e', '--environment', required=False, help='Environment')
@click.option('-a', '--alias', required=False, help='Alias. Overrules the database option')
@click.option('-v', '--version', required=False, help='The version to recreate')
@click.pass_obj
def cli(props, host, database, environment, alias, version):
    """
    Drop and recreate a MySQL database to the specified or latest version.
    """
    plugin = RecreatePlugin()
    plugin.execute(
        props,
        {
            'host': host, 'database': database, 'environment': environment,
            'alias': alias, 'version': version
        },
    )
