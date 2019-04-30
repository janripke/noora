import os

from noora.io.File import File
from noora.io.Filters import Filters
from noora.io.FileFolderFilter import FileFolderFilter
from noora.io.FileExtensionFilter import FileExtensionFilter
from noora.io.FileFilter import FileFilter


class Files(object):
    # FIXME: docstrings
    @staticmethod
    def list_filtered(folder, properties):
        filters = Filters()
        results = []

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
                    results.append(file)
        return results

    @staticmethod
    def list(file=None, recursive=False, exclude=None):
        result = []

        if file.exists():
            folder = file.get_url()
            file_list = os.listdir(folder)
            file_list.sort()
            for file_item in file_list:
                url = os.path.join(folder, file_item)
                candidate_file = File(url)
                if candidate_file.is_file() and exclude != "file":
                    result.append(candidate_file)
                if candidate_file.is_dir() and exclude != "directory":
                    result.append(candidate_file)
                if candidate_file.is_dir() and recursive == True:
                    recursive_files = Files.list(candidate_file, recursive, exclude)
                    for recursive_file in recursive_files:
                        result.append(recursive_file)
        return result
