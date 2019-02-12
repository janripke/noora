from noora.version.Version import Version


class Versions(object):
    def __init__(self):
        self.__versions = []

    def clear(self):
        self.__versions = []

    def size(self):
        return len(self.__versions)

    def sort(self):
        self.__versions.sort(key=lambda version: version.get_weight(), reverse=False)

    def add(self, version):
        versions = self.__versions
        versions.append(version)

    def exists(self, other):
        versions = self.__versions
        for version in versions:
            if version == other:
                return True
        return False

    def list(self):
        return self.__versions

    def previous(self, other):
        versions = self.__versions
        i = 0
        for version in versions:
            if version == other:
                if i == 0:
                    return version
                return versions[i - 1]
            i = i + 1

    def get_part(self, version):
        result = 0
        if version.has_major():
            result = result + 1
        if version.has_minor():
            result = result + 1
        if version.has_revision():
            result = result + 1
        if version.has_patch():
            result = result + 1
        return result

    def next(self):
        last = self.last()
        if last:
            level = self.get_part(last)
            major = last.get_major()
            minor = last.get_minor()
            revision = last.get_revision()
            patch = last.get_patch()
            if level == 1:
                major = str(int(major) + 1)
            if level == 2:
                minor = str(int(minor) + 1)
            if level == 3:
                revision = str(int(revision) + 1)
            if level == 4:
                patch = str(int(patch) + 1)

            if level == 1:
                version = major
            if level == 2:
                version = major + "." + minor
            if level == 3:
                version = major + "." + minor + "." + revision
            if level == 4:
                version = major + "." + minor + "." + revision + "." + revision

            return Version(version)

    def last(self):
        versions = self.__versions
        if versions:
            return versions[self.size() - 1]
