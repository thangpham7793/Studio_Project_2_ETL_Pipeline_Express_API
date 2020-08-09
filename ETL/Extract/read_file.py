import pandas as pd

switcher = {
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "csv": pd.read_csv,
    "txt": pd.read_csv,
}


def get_extension(file_path):
    """Return the extension from the supplied file path
    
    @param file_path: String
    @return ext: String
    
    Tests:
    
    Should return the correct extension when input is valid
    
    >>> get_extension('file.txt')
    'txt'
    >>> get_extension('file.xls')
    'xls'
    >>> get_extension('file.xlxs')
    'xlxs'
    >>> get_extension('file.csv')
    'csv'
    
    Should return the correct extension when input is valid even with multiple dots in file path
    
    >>> get_extension('file.file.txt')
    'txt'
    >>> get_extension('file.file.xls')
    'xls'
    >>> get_extension('file.file.xlxs')
    'xlxs'
    >>> get_extension('file.file.csv')
    'csv'
    
    Should throw an error when there's no dot in file name
    
    >>> get_extension('file_txt')
    File Path Must Have an Extension Followed by A Dot
    
    """
    try:
        has_dot_in_file_path = "." in file_path
    # user may forget to surround file path with quotes
    except NameError:
        print("File Path Must Be in Quotes")
    else:
        if has_dot_in_file_path == False:
            print("File Path Must Have an Extension Followed by A Dot")
        else:
            ext = file_path.split(".")[-1]
            return ext


def read_file(file_path):
    """ Use the appropriate pandas function to read a file based on its extension
    
    Should return KeyError when the file path contains an unknown extension
    >>> read_file('file.pdf')
    Unknown Extension. Please pick a file of type txt, xlxs, csv, or xls
    """
    ext = get_extension(file_path)

    # look up the appropriate pandas read file function
    try:
        file_reader = switcher[ext]
    except KeyError:
        print("Unknown Extension. Please pick a file of type txt, xlxs, csv, or xls")
        return

    # parse file into a dataframe
    try:
        if ext == "txt":
            # FIXME: a text file can have other types of delimiter
            df = file_reader(file_path, sep="|", encoding="unicode_escape")
        else:
            df = file_reader(file_path)
        return df
    except FileNotFoundError:
        print("File not found!")
        return


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
