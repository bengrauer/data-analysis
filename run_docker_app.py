import sys
from data_analysis.analysis import generate_analysis

if __name__ == '__main__':
    generate_analysis.run_analysis_routine(file_or_directory=sys.argv[1], output_directory=sys.argv[2])