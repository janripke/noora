#!/usr/bin/env python
import click

import noora

from noora.system.App import App


@click.command(cls=App, invoke_without_command=True, no_args_is_help=True)
@click.option('-r', '--revision', is_flag=True, help="Report the version of Noora and exit.")
@click.pass_context
def main(ctx, revision):
    """
    NoOra is a database deployment tool used to automate the database deployment cycle.
    """
    # show the revision
    if revision:
        print(noora.__title__ + " version " + noora.__version__)
        ctx.exit()


if __name__ == "__main__":
    main()
