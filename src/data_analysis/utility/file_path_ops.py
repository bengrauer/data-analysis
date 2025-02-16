import os
import errno
import pandas as pd


def check_is_directory(file_or_directory: str):
    func_name=check_is_directory.__name__
    if os.path.isdir(file_or_directory):
        print(f"{func_name}: directory determined.")
        return True
    else:
        return False


def directory_exists(directory: str, auto_create: bool):
    func_name = directory_exists.__name__
    try:
        if os.path.exists(directory) == False:
            if auto_create:
                print(f"{func_name}: Directory {directory} not found.  Attempting to create.")
                os.mkdir(directory)
        else:
            return True
    except OSError as os_error:
        raise
    return True


def append_analysis_directory(input_directory: str):
    func_name = append_analysis_directory.__name__
    analysis_directory = os.path.join(input_directory, "analysis")

    if not os.path.exists(analysis_directory):
        try:
            os.mkdir(analysis_directory)
            print(f"{func_name}: Directory created: {str(analysis_directory)}.")
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    else:
        print(f"{func_name}: Directory check - already exists: {str(analysis_directory)}.")

    return analysis_directory


def load_file(file_name: str):
    return pd.read_csv(file_name)


def check_is_file(file_or_directory: str):
    func_name = check_is_file.__name__
    if os.path.isfile(file_or_directory):
        print(f"{func_name}: single file determined")
        return True
    else:
        return False
