import click

from noora.plugins.postgresql.generate.GeneratePlugin import GeneratePlugin


@click.command()
@click.option('-v', '--version', required=False)
@click.pass_obj
def cli(props, version):
    """
    Bootstrap a new version of a PostgreSQL database project
    """
    plugin = GeneratePlugin()
    plugin.execute(props, {'version': version})


@click.command()
@click.option('-h', '--host', required=False, prompt=True, default='localhost')
@click.option('-p', '--port', required=False, prompt=True, type=int, default=5432)
@click.option('-d', '--database', required=True, prompt='Database name')
@click.option('-U', '--username', required=True, prompt='Database username')
@click.option('-P', '--password', required=True, prompt='Database password',
              hide_input=True, confirmation_prompt=True)
@click.option('-v', '--version', required=False,
              prompt='Initial project version', default='1.0.0')
@click.pass_obj
def cli_outside_scope(props, host, port, database, username, password, version):
    """
    Generate a new PostgreSQL database project
    """
    plugin = GeneratePlugin()
    plugin.execute(
        props,
        {
            'host': host, 'port': port, 'database': database,
            'username': username, 'password': password, 'version': version,
        },
    )
