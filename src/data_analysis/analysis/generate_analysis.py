# Author: Ben Grauer
# Created a python script that does some basic exploratory analysis / dov and exports to excel for easy viewing
# Designed for quick exploratory analysis of the data sets from Kaggle
import io
# imports
import os

from data_analysis.analysis.excel import (workbook_get_in_memory_file,
                                          add_sheet_summary_and_dov_pyspark,
                                          add_sheet_summary_and_dov_python,
                                          add_sheet_summary_ordered,
                                          add_sheet_correlation,
                                          add_sheet_covariance,
                                          add_sheet_samples_python,
                                          add_sheet_samples_spark)
from data_analysis.analysis.summary import generate_summary_stats_spark, generate_summary_stats_python
from data_analysis.utility.run_settings import RunSettings
from data_analysis.utility.run_settings import RunType, EnvRun
from data_analysis.utility.local_file_ops import load_file, workbook_write_in_memory_file_os


def run_analysis_cloud_spark(run_settings: RunSettings,
                             spark,
                             spark_df) -> None:
    func_name = run_analysis_cloud_spark.__name__
    generate_excel_workbook_spark(run_settings=run_settings, spark=spark, spark_df=spark_df)


def run_analysis_routine_local_csv(run_settings: RunSettings) -> None:
    func_name=run_analysis_routine_local_csv.__name__

    directory_to_evaluate = run_settings.input_dir

    for file_name in os.listdir(run_settings.input_dir):
        if len(file_name) > 3 and file_name[-4:] == '.csv':
            print(f"{func_name}: input file: {directory_to_evaluate + file_name}")
            output_file_name = os.path.join(run_settings.output_dir, ('analysis_' + str(file_name)[:-4] + '.xlsx'))
            print(f"{func_name}: file to generate: {output_file_name}")
            generate_excel_workbook_pandas(directory_to_evaluate + file_name, output_file_name)


def generate_excel_workbook_spark(run_settings: RunSettings,
                                  spark,
                                  spark_df) -> None:
    func_name = generate_excel_workbook_spark.__name__

    # set workbook
    workbook_bytes_io, workbook = workbook_get_in_memory_file()

    # obtain summary stats
    summary_df = generate_summary_stats_spark(spark, spark_df)

    # write sheets - only summary and samples for now
    add_sheet_summary_and_dov_pyspark(workbook, spark_df, summary_df)
    add_sheet_summary_ordered(workbook, summary_df)
    add_sheet_samples_spark(workbook, spark_df)

    # close + write
    workbook.close()
    write_excel_workbook_file(run_settings, workbook_bytes_io)
    print(f"{func_name}: excel workbook generated: {run_settings.output_file_name}")


def generate_excel_workbook_pandas(input_file_name: str,
                                   output_file_name: str) -> None:
    # Main function to load the file and generate the excel workbook
    func_name = generate_excel_workbook_pandas.__name__

    # pre-validate

    # set workbook
    run_settings = RunSettings(run_type=RunType.PYTHON, env_run=EnvRun.LOCAL,
                               input_dir=input_file_name, output_dir=output_file_name,
                               output_file_name=output_file_name)
    df = load_file(input_file_name)
    workbook_bytes_io, workbook = workbook_get_in_memory_file()

    # obtain summary stats
    summary_df = generate_summary_stats_python(df)

    # write sheets
    add_sheet_summary_and_dov_python(workbook, df, summary_df)
    add_sheet_summary_ordered(workbook, summary_df)
    add_sheet_correlation(workbook, df)
    add_sheet_covariance(workbook, df)
    add_sheet_samples_python(workbook, df)

    # close
    workbook.close()
    run_settings.output_file_name = output_file_name
    write_excel_workbook_file(run_settings, workbook_bytes_io)
    print(f"{func_name}: excel workbook generated: {output_file_name}")


def write_excel_workbook_file(run_settings: RunSettings,
                              workbook_bytes_io: io.BytesIO) -> None:
    func_name = write_excel_workbook_file.__name__

    print(f"{func_name}: Writing to environment: {run_settings.run_type}")

    if run_settings.env_run == EnvRun.LOCAL:
        workbook_write_in_memory_file_os(output_file_name=run_settings.output_file_name,
                                         file_bytes_io=workbook_bytes_io)

    elif run_settings.env_run == EnvRun.AZURE:
        from data_analysis.utility.azure_file_ops import upload_file_from_bytes_in_chunks
        upload_file_from_bytes_in_chunks(run_settings=run_settings,
                                         file_bytes_io=workbook_bytes_io)

    elif run_settings.env_run == EnvRun.AWS:
        from data_analysis.utility.aws_file_ops import upload_file_from_bytes
        upload_file_from_bytes(run_settings=run_settings,
                               file_bytes_io=workbook_bytes_io)

    else:
        print(f"{func_name}: run type not recognized: {run_settings.run_type}")
