from noora.version.versions import Versions
from noora.version.version import Version

# def weight(value):
#     i = 0
#     result = 0
#     print value.split('.')
#     for item in value.split('.'):
#
#         result = result + float(item) / 1000**i
#         print result
#         i = i + 1
#     return result
#
#
# print weight('1.0.3.2')

versions = Versions()

version = Version("1.0.2")
versions.add(version)

version = Version("1.0.3")
versions.add(version)

version = Version("1.0.3.1")
versions.add(version)

version = Version("1.0.3.2")
versions.add(version)

version = Version("1.0.4")
versions.add(version)

version = Version("1.0.1")
versions.add(version)

versions.sort()

for version in versions.list():
    print version.get_weight(), version.to_string()