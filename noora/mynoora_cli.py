#!/usr/bin/env python
import noora
import argparse


def main(args=None):
    # Instantiate the parser
    parser = argparse.ArgumentParser(description="mynoora, a mysql deployment tool")
    parser.add_argument('-v', action='store_true', help='show the version')
    parser.add_argument('input', action='append')

    args = parser.parse_args(args)
    print args
    if args.v:
        print noora.__title__ + " version " + noora.__version__
        exit(0)


if __name__ == "__main__":
    main(args=None)


