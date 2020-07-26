# TODO: need to be able to read all file extensions?

import pandas as pd
import os
from overview_helpers import check_colnames
from string import Template


def overview(folder_path, file_path, extension):
    # print("It's", extension)
    switcher = {
        "excel": pd.read_excel,
        "csv": pd.read_csv,
    }

    # read, replace na values and check colnames

    df = switcher.get(extension)(file_path)
    df = df.fillna("no record")
    df = check_colnames(df)

    # format the name of the output file
    file_name = file_path.replace(folder_path, "")
    file_name = file_name.replace(".xls", "")
    overview_name = "{}_overview.txt".format(file_name)
    # print("Examining " + file_name)
    # make a folder to store all the overview file
    overview_dir = "./overview/{}".format(overview_name)
    os.makedirs(os.path.dirname(overview_dir), exist_ok=True)

    # open and start writing the relevant info
    with open(overview_dir, "w") as f:

        f.write("Columns: " + str(list(df.columns)) + "\n\n\n")

        f.write("Number of Rows and Cols: " + str(df.shape) + "\n\n\n")

        for col in df.columns:
            # only write out columns with less than 500 unique values
            if len(df[col].unique()) < 500:
                f.write(str(col) + ": " + str(list(df[col].unique())) + "\n\n\n")
        f.close()
    return list(df.columns)


def make_table_overview(folder_path):
    # to make sure that it writes the result file in the current directory rather than the home dir
    if folder_path.endswith("/") == False:
        folder_path = folder_path + "/"
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and (
            file_path.endswith(".xls") or file_path.endswith(".xlsx")
        ):
            try:
                cols = overview(folder_path, file_path, "excel")
                write_colnames(cols)
            except:
                print("Could not process file", file_path)
        elif os.path.isfile(file_path) and file_path.endswith(".csv"):
            try:
                cols = overview(folder_path, file_path, "csv")
                write_colnames(cols)
            except:
                print("Could not process file", file_path)
        # continue to open other folders inside and do the same thing
        elif os.path.isdir(file_path):
            make_table_overview(file_path)


def write_colnames(cols):
    f = open("./overview/colnames.txt", "a")
    colnames = str(list(cols))
    colnames = colnames.replace("[", ",")
    colnames = colnames.replace("]", ",")
    f.write(colnames)
    f.close()


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


"""
    SECOND VERSION STARTS HERE (RESULT BEING AN HTML FILE)
"""

from classes.Load import Load

folder_path = "./data/Pit-Dump Locations"
loader = Load()


def make_data_overview(folder_path):
    # to make sure that it writes the result file in the current directory rather than the home dir
    if folder_path.endswith("/") == False:
        folder_path = folder_path + "/"
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
                loader.to_df(file_path)
            except:
                print("Could not process file", file_path)
        # continue to open other folders inside and do the same thing
        elif os.path.isdir(file_path):
            make_data_overview(file_path)


overview_template = Template(
    """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="log_style.css" />
    <title>Overview of All Tabular Data</title>
  </head>
  <body>
    <header>
        <h1><a id="Top">Pit Dump Locations Overview</a></h1>
    </header>
    <div>
        <ul class='index-nav-list'>
            ${top_nav_list}
        </ul>
    </div>
    <div>
        <nav>
        <ul>
            ${links_to_log_pages}
        </ul>
        </nav>
    </div>
    <footer>
      <small>
        <a href="#Top">Back to top</a>
      </small>
    </footer>
  </body>
</html>

"""
)


def make_anchor(folder_path):
    if folder_path.endswith("/") == False:
        folder_path = folder_path + "/"
    anchor_list = ""
    state_name = folder_path.split("/")[-2]
    for f in os.listdir(folder_path):
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path):
            anchor_list += f"""<li><a href="{file_path}">{file_path.split('/')[-1].split('.')[0]}</a></li>"""

    return f"""<li><a id='{state_name}'>{state_name}</a><ul>{anchor_list}<li><a href="#Top">Back to top</a></li></ul></li>"""


def make_overview_html_index():
    log_folder = "./logs"
    links_to_log_pages = ""
    top_nav_list = ""
    for folder in os.listdir(log_folder):
        folder_path = os.path.join(log_folder, folder)
        links_to_log_pages += make_anchor(folder_path)
        top_nav_list += f'<li><a href="#{folder}">{folder}</a></li>'

    html = overview_template.substitute(
        top_nav_list=top_nav_list, links_to_log_pages=links_to_log_pages
    )
    f = open("index.html", "w")
    f.write(html)
    f.close()
