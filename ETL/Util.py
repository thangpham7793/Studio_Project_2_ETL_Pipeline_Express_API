import sys
import os
import pandas as pd

result = ""


def pipe_and_apply(next_input, steps_list):
    global result
    while len(steps_list) != 0:
        resources = steps_list.pop(0)
        step = resources["step"]
        function = resources["function"]
        print(f"{step} in progress...\n")
        output = function(next_input)
        result = output
        if isinstance(output, pd.DataFrame) and output.empty == False:
            print(f"{step} completed!\n")
            # print(output.head(2), "\n", "=" * 120)
            pipe_and_apply(output, steps_list)
        else:
            print(f"\nCould not finish {step} step. Invalid input: \n\n {output}")
            return
    return result


# a higher-order function that returns a customized function that recursively
# applies a function to all file within a directory


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


def make_pipeline(next_input, steps_list):
    def run_pipeline():
        return pipe_and_apply(next_input, steps_list)

    return run_pipeline


# delete all files with unwanted extension recursively in a folder
def clean_up(dir):
    ext_list = []
    for f in os.listdir(dir):
        f_path = os.path.join(dir, f)
        ext = f_path.split(".")[-1]
        kept = ["csv", "txt", "xlsx", "xls"]
        if os.path.isfile(f_path) and ext not in kept:
            print("Deleting", f_path)
            os.remove(f_path)
        elif os.path.isdir(f_path):
            if len(os.listdir(dir)) == 0:
                print("Deleting empty dir", dir)
                os.rmdir(dir)
            clean_up(f_path)


def reset_schema(schema_path):
    f = open(schema_path, "r")

