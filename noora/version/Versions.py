from noora.version.Version import Version


class Versions(object):
    """
    Management class for handling versions of a project. Useful for inspecting
    and testing the versions on a project and to manage updating projects to
    specific versions.
    """
    def __init__(self):
        self.__versions = []

    def clear(self):
        """Remove all versions from the class"""
        self.__versions = []

    def sort(self):
        """Sort the versions by weight"""
        self.__versions.sort(key=lambda version: version.get_weight(), reverse=False)

    def add(self, version):
        """Add a version to the list"""
        versions = self.__versions
        versions.append(version)

    def exists(self, other):
        """Check if the specified version exists"""
        versions = self.__versions
        for version in versions:
            if version == other:
                return True
        return False

    def list(self):
        """Return the list of versions"""
        return self.__versions

    def previous(self, other):
        """Return the version that precedes the provided version"""
        versions = self.__versions
        i = 0
        for version in versions:
            if version == other:
                if i == 0:
                    return version
                return versions[i - 1]
            i = i + 1

    def get_part(self, version):
        """Return the number of parts in the specified version"""
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
        """
        Calculate the next version number based on the last version in the
        list, incrementing the smallest version component by one depending on the
        number of parts.
        """
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
            elif level == 2:
                version = major + "." + minor
            elif level == 3:
                version = major + "." + minor + "." + revision
            elif level == 4:
                version = major + "." + minor + "." + revision + "." + patch
            # Higher levels are not supported
            else:
                # FIXME: raise exception?
                return None

            return Version(version)

        # If no version was found, return nothing.
        return None

    def last(self):
        """Return the last version in the list"""
        versions = self.__versions
        if versions:
            return versions[-1]
