import errno
import os

import pandas as pd


def check_is_directory(file_or_directory):
    if os.path.isdir(file_or_directory):
        print('processing - directory determined')
        return True
    else:
        return False


def directory_exists(input_directory):
    return os.path.exists(input_directory)


def append_analysis_directory(input_directory):
    analysis_directory = os.path.join(input_directory, "analysis")

    if not os.path.exists(analysis_directory):
        try:
            os.mkdir(analysis_directory)
            print("Directory created: " + str(analysis_directory))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    else:
        print('directory check - already exists: ' + str(analysis_directory))

    # return the analysis directory
    return analysis_directory


def load_file(file_name):
    return pd.read_csv(file_name)


def check_is_file(file_or_directory):
    if os.path.isfile(file_or_directory):
        print('processing - single file determined')
        return True
    else:
        return False
