from noora.io.File import File
import os


class Files:
    def __init__(self):
        pass

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
