from src.data_analysis.utility.file_path_ops import (check_is_directory,
                                                     directory_exists,
                                                     append_analysis_directory,
                                                     load_file,
                                                     check_is_file)


def test_check_is_directory_pass():
    assert check_is_directory("../data/input/")
def test_check_is_directory_fail():
    assert check_is_directory("../data/output/sub_directory/") is False

def test_directory_exists_pass():
    assert directory_exists("../data/output/", auto_create=True)
def test_directory_exists_fail():
    assert directory_exists("../data/output/sub_directory/", auto_create=True) is False

def test_append_analysis_directory_pass():
    assert append_analysis_directory("../data/output/") == "../data/output/analysis"

def test_load_file_pass():
    assert len(load_file("../data/input/sample_data.csv")) > 1

def test_check_is_file_pass():
    assert check_is_file("../data/input/sample_data.csv")