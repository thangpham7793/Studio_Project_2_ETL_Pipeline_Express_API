import sys
import os


class Util:

    # a higher-order function that returns a customized function that recursively
    # applies a function to all file within a directory
    @staticmethod
    def apply_on_all_files(func):
        def customized_func(folder_path):
            if folder_path.endswith("/") == False:
                folder_path = folder_path + "/"
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    try:
                        func(file_path)
                    except:
                        print(f"Could not process file: {sys.exc_info()}")
                # continue to open other folders inside and do the same thing
                elif os.path.isdir(file_path):
                    customized_func(file_path)

        return customized_func

