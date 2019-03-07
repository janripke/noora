#!/usr/bin/env python
import click

import noora

from noora.system.App import App


@click.command(cls=App, invoke_without_command=True, no_args_is_help=True)
@click.option('-r', '--revision', is_flag=True)
def main(revision):
    # show the revision
    if revision:
        print(noora.__title__ + " version " + noora.__version__)
        return


if __name__ == "__main__":
    main()
