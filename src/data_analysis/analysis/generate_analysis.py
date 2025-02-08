# Author: Ben Grauer
# Created a python script that does some basic exploratory analysis / dov and exports to excel for easy viewing
# Designed for quick exploratory analysis of the data sets from Kaggle

# imports
import os

from data_analysis.analysis.excel import generate_excel_workbook
from data_analysis.utility.file_path_ops import (check_is_directory,
                                                 directory_exists,
                                                 append_analysis_directory,
                                                 check_is_file)


def run_analysis_routine(file_or_directory: str, output_directory: str):
    directory_to_evaluate = ""

    if check_is_file(file_or_directory):
        is_file_to_analyze = True
        is_path_to_analyze = False
    elif check_is_directory(file_or_directory):
        is_path_to_analyze = True
        is_file_to_analyze = False
        directory_to_evaluate = file_or_directory
    else:
        raise Exception(f"Error - Invalid file or path passed in.  {file_or_directory}")

    if not directory_exists(directory=output_directory, auto_create=True):
        raise Exception(f"Error - Invalid output directory passed in.  {output_directory}")

    if is_path_to_analyze:
        if not output_directory:
            output_directory = append_analysis_directory(directory_to_evaluate)

        for file_name in os.listdir(file_or_directory):
            if len(file_name) > 3 and file_name[-4:] == '.csv':
                print('input file: ' + directory_to_evaluate + file_name)
                output_file_name = os.path.join(output_directory, ('analysis_' + str(file_name)[:-4] + '.xlsx'))
                print('file to generate: ' + output_file_name)
                generate_excel_workbook(directory_to_evaluate + file_name, output_file_name)

    elif is_file_to_analyze:
        file_name = os.path.basename(file_or_directory)
        input_directory = os.path.dirname(file_or_directory)
        if not output_directory:
            output_directory = append_analysis_directory(input_directory)
        output_file_name = os.path.join(output_directory, ('analysis_' + str(file_name)[:-4] + '.xlsx'))
        print('file to generate: ' + output_file_name)
        generate_excel_workbook(file_or_directory, output_file_name)
