import sys
import os
from os import system, name
from string import Template


def pipe_and_apply(next_input, stages_list):
    print(f"Starting the next stage!\n")
    while len(stages_list) != 0:
        tools = stages_list.pop(0)
        stage = tools["stage"]
        function = tools["function"]

        try:
            print(f"{stage} started!\n")
            output = function(next_input)
            print(f"{stage} completed!\n")
            pipe_and_apply(next_input, stages_list)
        except:
            print(f"Could not finish {stage} stage: {sys.exc_info()}")
            return

    print("Finished the whole process!")


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
    def connect_pipeline(next_input, stages_list):
        def run_pipeline():
            pipe_and_apply(next_input, stages_list)

        return run_pipeline

    @staticmethod
    # https://www.geeksforgeeks.org/clear-screen-python/
    def clear_screen():
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")

    @staticmethod
    def update_schema():
        f = open("schema.py", "w")
        f.write(f"mine_schema = {mine_schema}")
        f.close()


def generate_function_documentation(definition_dict):
    function_task_template = Template("This function ${task}\n")
    param_definition_template = Template("@param ${name}: ${type}\n")
    return_value_definition_template = Template("@return '${name}': ${type}\n")

    description = ""
    try:
        for k in definition_dict:
            if k == "task":
                description += function_task_template.substitute(
                    task=definition_dict["task"]
                )
            elif k == "return":
                description += return_value_definition_template.substitute(
                    name=k, type=definition_dict[k]
                )
            else:
                description += param_definition_template.substitute(
                    name=k, type=definition_dict[k]
                )

        print(description)
    except TypeError as e:
        print("Please supply a dictionary for the definition")


def get_documentation(definition_dict):
    def print_definition():
        generate_function_documentation(definition_dict)

    return print_definition
