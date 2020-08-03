import sys
import os
import pandas as pd


def pipe_and_apply(next_input, steps_list):
    while len(steps_list) != 0:
        resources = steps_list.pop(0)
        step = resources["step"]
        function = resources["function"]
        print(f"{step} started!\n")
        output = function(next_input)
        if isinstance(output, pd.DataFrame) and output.empty == False:
            print(f"{step} completed!\n")
            print(output.head(5), "\n", "=" * 120)
            pipe_and_apply(output, steps_list)
        else:
            print(f"\nCould not finish {step} step: {sys.exc_info()}")
            return


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
                    except AttributeError:
                        print(f"Could not process file: {sys.exc_info()}")
                # continue to open other folders inside and do the same thing
                elif os.path.isdir(file_path):
                    customized_func(file_path)

        return customized_func

    # higher order function that returns a ready-to-run pipeline
    @staticmethod
    def make_pipeline(next_input, steps_list):
        def run_pipeline():
            pipe_and_apply(next_input, steps_list)

        return run_pipeline

