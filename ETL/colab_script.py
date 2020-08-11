# !python -m pip install fuzzywuzzy python-Levenshtein pymongo[srv]
# run this cell first to install missing packages

# import python libs
import sys
import os

# add parser to path so that main.ipynb can find it
parser_path = "/content/drive/My Drive/ETL"
sys.path.append(f"{parser_path}")

# The packages below are used for file uploading
from google.colab import files

# import parser function
from main import main


def run_main():
    print()
    print("Please upload a csv, excel, or txt file from your computer.")
    # upload widget
    file = files.upload()

    # get file name from the uploaded file
    try:
        file_name = list(file.keys())[0]
    except IndexError as e:
        print(f"Could not determine file name.\n")
        return
    # use os to find absoulute path
    path = os.path.abspath(file_name)

    # run parser
    main(path)


def menu():
    # start the parser
    run_main()
    # ask if user wants to process another file:
    invalid_input = True
    process_another = True
    while process_another:
        answer = input("Would you like to process another data set? Y/N \n")
        while invalid_input:
            if answer.lower() not in ["y", "ye", "yes", "n", "no"]:
                print("Invalid input. Please type Yes or No.")
            else:
                invalid_input = False
        # execute according to user's answer
        if answer.lower() in ["y", "ye", "yes"]:
            # run and reset checks
            run_main()
            invalid_input = True
            process_another = True
        else:
            process_another = False
            print("Bye")
            break


menu()
