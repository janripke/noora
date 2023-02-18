import argparse
from noora.plugins.mysql.create.create_plugin import CreatePlugin

parser = argparse.ArgumentParser(description="mynoora, a mysql deployment tool", add_help=False)
parser.add_argument("commands", help="display a square of a given number", type=str, nargs='+')
parser.add_argument('-r', action='store_true', help='show the revision')


arguments, unknown = parser.parse_known_args(['create', '-h', 'localhost'])


parser.add_argument('-v', type=str, help='version', required=False)
parser.add_argument('-h', type=str, help='host', required=False)
parser.add_argument('-d', type=str, help='database', required=False)
parser.add_argument('-e', type=str, help='environment', required=False)
parser.add_argument('-a', type=str, help='alias', required=False)

arguments = parser.parse_args(['create', '-h', 'localhost'])
host = arguments.h
print(host)

plugin = CreatePlugin()
plugin.set_connector()
# if __name__ == '__main__':
#     unittest.main()
