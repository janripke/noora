from noora.io.filters import Filters
from noora.io.file import File
from noora.io.files import Files
from noora.io.file_folder_filter import FileFolderFilter
from noora.io.file_extension_filter import FileExtensionFilter
from noora.io.file_filter import FileFilter


class ConnectionExecutor(object):
    """
    This class unlocks functionality to execute a list of files in a
    specified folder, supporting file, folder and extension filtering.
    """
    @staticmethod
    def execute(connector, executor, properties, folder):
        """
        Execute all applicable files in the specified folder.

        :type connector: noora.connectors.connector.Connector
        :param connector: A connector instance;
        :type executor: dict
        :param executor: Settings and credentials for the connector;
        :type properties: noora.system.properties.Properties
        :param properties: Project properties;
        :param folder: The target folder to execute.
        """
        filters = Filters()

        excluded_folders = properties.get('excluded_folders')
        for excluded_folder in excluded_folders:
            ef = File(excluded_folder)
            ff = FileFolderFilter(ef)
            filters.add(ff)

        excluded_extensions = properties.get('excluded_extensions')
        for excluded_extension in excluded_extensions:
            ef = File("*." + excluded_extension)
            ff = FileExtensionFilter(ef)
            filters.add(ff)

        excluded_files = properties.get('excluded_files')
        for excluded_file in excluded_files:
            ef = File(excluded_file)
            ff = FileFilter(ef)
            filters.add(ff)

        if folder.is_dir():
            files = Files.list(folder)
            for file in files:
                if not filters.accept(file) and not file.is_dir():
                    url = file.get_url()
                    print(url)
                    executor['script'] = file
                    connector.execute(executor, properties)
