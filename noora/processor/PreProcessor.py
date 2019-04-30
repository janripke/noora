class PreProcessor(object):
    """Template parser"""
    @staticmethod
    def parse(file, properties):
        """
        Parse the template and replace all keys if applicable.

        :type file: noora.io.File.File
        :param file: The file to process;
        :type properties: dict
        :param properties: All keys to replace in the file with their respective values;

        :return: The parsed file as a string.
        """
        f = open(file.get_url())
        stream = f.read()
        f.close()

        for key in properties.keys():
            if properties.get(key):
                stream = stream.replace("{" + key + "}", properties.get(key))

        return stream
