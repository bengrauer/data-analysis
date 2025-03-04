import pytest

from src.data_analysis.analysis.excel import (workbook_get_physical_file,
                                               workbook_get_in_memory_file)
from src.data_analysis.utility.local_file_ops import workbook_write_in_memory_file_os



def test_workbook_get_physical_file_pass():
    assert workbook_get_physical_file(output_file_name="../data/output/sample_data.xlsx") is not None


def test_workbook_write_in_memory_file_os_pass():
    workbook_bytes_io, workbook = workbook_get_in_memory_file()
    workbook_write_in_memory_file_os(output_file_name="../data/output/sample_data.xlsx",
                                     file_bytes_io=workbook_bytes_io)
    assert True
