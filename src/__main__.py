# Author: Ben Grauer
# Created a python script that does some basic exploratory analysis / dov and exports to excel for easy viewing
# Designed for quick exploratory analysis of the data sets from Kaggle

# imports
import sys

from generate_analysis import run_analysis_routine

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print('arg 1: ' + str(sys.argv[1]))
        file_or_directory = sys.argv[1]

    file_or_directory = "/media/data/project/data/kg_RussiaHousing/train.csv"
    run_analysis_routine(file_or_directory)