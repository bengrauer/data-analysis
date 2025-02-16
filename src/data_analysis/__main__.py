# Author: Ben Grauer
# Created a python script that does some basic exploratory analysis / dov and exports to excel for easy viewing
# Designed for quick exploratory analysis of the data sets from Kaggle

# imports
import sys
import argparse

from data_analysis.analysis.generate_analysis import run_analysis_routine


def read_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="The parsing commands lists.")
    parser.add_argument("-i", "--input_file_dir", help="Input File or Directory.")
    parser.add_argument("-o", "--output_dir", help="Output Directory.")

    opts = parser.parse_args(args)
    return opts


if __name__ == '__main__':
    func_name="__main__"

    if len(sys.argv) > 1:
        print(f"{func_name}: sys.argv[1]: {str(sys.argv[1])}")
        file_or_directory = sys.argv[1]

    if len(sys.argv) > 2:
        print(f"{func_name}: sys.argv[2]: {str(sys.argv[2])}")
        output_directory = sys.argv[2]

    options = read_options(sys.argv[1:])

    if options.input_file_dir:
        file_or_directory = options.input_file_dir
        print(f"{func_name}: options.input_file_dir: {options.input_file_dir}")
    else:
        file_or_directory = ""

    if options.output_dir:
        output_directory = options.output_dir
        print(f"{func_name}: options.output_dir: {options.output_dir}")
    else:
        output_directory = ""

    run_analysis_routine(file_or_directory=file_or_directory,
                         output_directory=output_directory)
