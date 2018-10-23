class PreProcessor:
    def __init__(self):
        pass

    @staticmethod
    def parse(file, properties):
        f = open(file.get_url())
        stream = f.read()
        f.close()

        for key in properties.keys():
            if properties.get(key):
                stream = stream.replace("{" + key + "}", properties.get(key))

        return stream
