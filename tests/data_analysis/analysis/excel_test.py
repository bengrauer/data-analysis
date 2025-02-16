from src.data_analysis.analysis.excel import (workbook_get_physical_file,
                                              workbook_get_in_memory_file,
                                              workbook_write_in_memory_file_os)


def test_workbook_get_physical_file_pass():
    assert workbook_get_physical_file(output_file_name="../data/output/sample_data.xlsx") is not None

def test_workbook_get_in_memory_file_pass():
    assert workbook_get_in_memory_file() is not None

def test_workbook_write_in_memory_file_os_pass():
    assert workbook_write_in_memory_file_os(output_file_name="sample_data.xlsx",
                                            workbook_bytes_io=workbook_get_in_memory_file())
