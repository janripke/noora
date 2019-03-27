from importlib import import_module


class ClassLoader(object):
    @staticmethod
    def find_plugin(technology, name):
        """
        Find a plugin based on the technology and the name. Note that this is
        a 'dumb' method that only builds up the module path.

        :param technology: Technology to look in for the plugin
        :param name: Name of the plugin
        :return: A module path including class name
        """
        plugin_class = '{}Plugin'.format(name.lower().capitalize())

        return 'noora.plugins.{}.{}.{}.{}'.format(technology, name, plugin_class, plugin_class)

    @staticmethod
    def load_class(pattern):
        """
        Import the class from the pattern and return an instance of the class.
        :param pattern: Full python module path including the class name

        :return: Class instance
        """
        pattern_list = pattern.rsplit(".", 1)
        if len(pattern_list) < 2:
            raise ValueError(
                'A class pattern should consist of at least one module and a classname')

        mod_path = pattern_list[0]
        class_name = pattern_list[1]

        mod = import_module(mod_path)
        cls = getattr(mod, class_name)
        instance = cls()

        return instance
