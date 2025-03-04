# system imports
import numpy as np
import pandas
import pandas as pd
from io import BytesIO
from typing import Any

# external package imports
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

# project imports
from data_analysis.analysis.summary import ROUND_PRECISION
from data_analysis.analysis.summary import is_spark_numeric_data_type


# constants for sheet summary and dov header
const_sum_dov_col_name_row = 0
const_sum_dov_data_type_row = 1
const_sum_dov_count_row = 2
const_sum_dov_num_nan_row = 3
const_sum_dov_nan_perc_row = 4

const_sum_dov_mean_row = 5
const_sum_dov_median_row = 6
const_sum_dov_std_row = 7
const_sum_dov_var_row = 8
const_sum_dov_range_row = 9
const_sum_dov_0_prct_row = 10
const_sum_dov_25_prct_row = 11
const_sum_dov_50_prct_row = 12
const_sum_dov_75_prct_row = 13
const_sum_dov_100_prct_row = 14

const_sum_dov_cont_or_desc_row = 16
const_sum_dov_notes_row = 17

const_sum_dov_row_data_header = 19
const_sum_dov_row_freeze_row = 19


def workbook_get_physical_file(output_file_name) -> xlsxwriter.Workbook:
    # get the workbook for an os physical file
    return xlsxwriter.Workbook(output_file_name, {'nan_inf_to_errors': True})


def workbook_get_in_memory_file() -> tuple[BytesIO, xlsxwriter.Workbook]:
    # get in memory workbook
    workbook_bytes_io = BytesIO()
    return workbook_bytes_io, xlsxwriter.Workbook(workbook_bytes_io)


def worksheet_add_df(input_workbook: xlsxwriter.Workbook,
                     input_worksheet: xlsxwriter.Workbook.worksheet_class,
                     input_sheet_name: str,
                     input_dataframe: pandas.DataFrame,
                     input_start_row: int = 0,
                     input_start_col: int = 0,
                     input_use_index: bool = False) -> None:
    # Generic function to add a dataframe to a worksheet

    bold = input_workbook.add_format({'bold': True})
    font14bold = input_workbook.add_format({'font_size': 14, 'bold': True})

    row_num = input_start_row
    col_num = input_start_col

    input_worksheet.write(row_num, input_start_col, input_sheet_name, font14bold)
    row_num += 1

    if input_use_index:
        input_worksheet.write_column(input_start_row + 3, col_num, input_dataframe.index, bold)
        col_num += 1

    for column in input_dataframe:
        row_num = input_start_row + 2
        input_worksheet.write(row_num, col_num, input_dataframe[column].name, bold)

        row_num = input_start_row + 3
        input_worksheet.write_column(row_num, col_num, input_dataframe[column])

        col_num += 1


def add_sheet_summary_and_dov_header(worksheet: xlsxwriter.Workbook.worksheet_class,
                                     bold) -> None:
    # Function to add header information to summary and dov sheet
    worksheet.write(const_sum_dov_col_name_row, 0, 'Col Name', bold)
    worksheet.write(const_sum_dov_data_type_row, 0, 'Data Type', bold)
    worksheet.write(const_sum_dov_count_row, 0, 'count', bold)
    worksheet.write(const_sum_dov_num_nan_row, 0, 'NaN', bold)
    worksheet.write(const_sum_dov_nan_perc_row, 0, 'NaN %', bold)
    worksheet.write(const_sum_dov_mean_row, 0, 'mean', bold)
    worksheet.write(const_sum_dov_median_row, 0, 'median', bold)
    worksheet.write(const_sum_dov_std_row, 0, 'std', bold)
    worksheet.write(const_sum_dov_var_row, 0, 'var', bold)
    worksheet.write(const_sum_dov_range_row, 0, 'range', bold)
    worksheet.write(const_sum_dov_0_prct_row, 0, '0%', bold)
    worksheet.write(const_sum_dov_25_prct_row, 0, '25%', bold)
    worksheet.write(const_sum_dov_50_prct_row, 0, '50%', bold)
    worksheet.write(const_sum_dov_75_prct_row, 0, '75%', bold)
    worksheet.write(const_sum_dov_100_prct_row, 0, '100%', bold)

    worksheet.write(const_sum_dov_cont_or_desc_row, 0, 'Var Type')
    worksheet.write(const_sum_dov_notes_row, 0, 'Notes')


def add_sheet_summary_and_dov_python(workbook: xlsxwriter.Workbook,
                                     df: pandas.DataFrame,
                                     summary_df: pandas.DataFrame) -> None:
    # Adds the main summary, domain of values and distribution percentages
    func_name = add_sheet_summary_and_dov_python.__name__

    worksheet = workbook.add_worksheet('DOV')

    bold = workbook.add_format({'bold': True})
    italic = workbook.add_format({'italic': True})
    underline = workbook.add_format({'underline': True})
    format_high = workbook.add_format({'font_color': 'red'})
    format_low = workbook.add_format({'font_color': 'blue'})

    col_iteration = 1
    row_iteration = 0
    row_data_header = const_sum_dov_row_data_header

    add_sheet_summary_and_dov_header(worksheet, bold=bold)

    for column in df:
        print(f"{func_name}: adding column {column} information.")
        worksheet.write(row_iteration, col_iteration, df[column].name, bold)
        worksheet.write(const_sum_dov_data_type_row, col_iteration, str(df[column].dtypes))

        worksheet.write(const_sum_dov_count_row, col_iteration, summary_df.loc['count'][column])
        worksheet.write(const_sum_dov_num_nan_row, col_iteration, summary_df.loc['total_null'][column])
        worksheet.write(const_sum_dov_nan_perc_row, col_iteration, summary_df.loc['total_null_perc'][column])

        if np.issubdtype(df[column].dtype, np.number):
            worksheet.write(const_sum_dov_mean_row, col_iteration, summary_df.loc['mean'][column])
            worksheet.write(const_sum_dov_median_row, col_iteration, summary_df.loc['median'][column])
            worksheet.write(const_sum_dov_std_row, col_iteration, summary_df.loc['std'][column])
            worksheet.write(const_sum_dov_var_row, col_iteration, summary_df.loc['var'][column])
            worksheet.write(const_sum_dov_range_row, col_iteration, summary_df.loc['range'][column])
            worksheet.write(const_sum_dov_0_prct_row, col_iteration, summary_df.loc['0%'][column])
            worksheet.write(const_sum_dov_25_prct_row, col_iteration, summary_df.loc['25%'][column])
            worksheet.write(const_sum_dov_50_prct_row, col_iteration, summary_df.loc['50%'][column])
            worksheet.write(const_sum_dov_75_prct_row, col_iteration, summary_df.loc['75%'][column])
            worksheet.write(const_sum_dov_100_prct_row, col_iteration, summary_df.loc['100%'][column])

        worksheet.write(row_data_header - 1, col_iteration, 'DOV', underline)
        worksheet.write(row_data_header - 1, col_iteration + 1, 'DistPrc', underline)

        const_data_type_continuous = 'continuous'
        const_data_type_categorical = 'categorical'
        const_data_type_discrete = 'discrete'

        var_type = const_data_type_continuous
        worksheet.write(const_sum_dov_cont_or_desc_row, col_iteration, const_data_type_continuous)

        if df[column].nunique() > 500:
            if np.issubdtype(df[column].dtype, np.number):
                var_type = const_data_type_continuous
            else:
                var_type = const_data_type_categorical
        else:
            if df[column].nunique() < 100:
                if np.issubdtype(df[column].dtype, np.number):
                    var_type = const_data_type_discrete
                else:
                    var_type = const_data_type_categorical
            else:
                var_type = const_data_type_categorical

        worksheet.write(row_iteration + const_sum_dov_cont_or_desc_row, col_iteration, var_type)

        disb_df = pd.DataFrame(df.groupby([column]).size() * 100 / len(df)).round(ROUND_PRECISION)
        disb_df.rename(columns={0: 'distprc'}, inplace=True)
        disb_df = disb_df.sort_values(['distprc'], ascending=False)
        disb_df = disb_df.rename_axis('dov').reset_index().copy()

        if df[column].nunique() > 500:
            worksheet.write(row_data_header, col_iteration, '> 500 unq', italic)
            worksheet.write_column(row_data_header + 1, col_iteration, disb_df.loc[:, 'dov'].head(100))
            col_iteration += 1

            worksheet.write(row_data_header, col_iteration, '> 500 unq')
            worksheet.write_column(row_data_header + 1, col_iteration, disb_df.loc[:, 'distprc'].head(100))
            col_iteration += 1
        else:
            worksheet.write_column(row_data_header, col_iteration, disb_df.loc[:, 'dov'])
            col_iteration += 1

            worksheet.write(row_data_header, col_iteration, 'DistPrc')
            worksheet.write_column(row_data_header, col_iteration, disb_df.loc[:, 'distprc'])
            col_iteration += 1

    worksheet.freeze_panes(const_sum_dov_row_data_header, 1)

    print(f"{func_name}: sheet completed - DOV")


def add_sheet_summary_and_dov_pyspark(workbook: xlsxwriter.Workbook,
                                      spark_df,
                                      summary_df: pandas.DataFrame) -> None:
    # Adds the main summary, domain of values and distribution percentages
    # df is a pyspark.sql.dataframe
    from pyspark.sql import functions as f

    func_name = add_sheet_summary_and_dov_python.__name__

    worksheet = workbook.add_worksheet('DOV')

    bold = workbook.add_format({'bold': True})
    italic = workbook.add_format({'italic': True})
    underline = workbook.add_format({'underline': True})
    format_high = workbook.add_format({'font_color': 'red'})
    format_low = workbook.add_format({'font_color': 'blue'})

    col_iteration = 1
    row_iteration = 0
    row_data_header = const_sum_dov_row_data_header

    add_sheet_summary_and_dov_header(worksheet, bold=bold)

    summary_df.set_index("metric", inplace=True)

    for column in summary_df:
        print(f"{func_name}: adding column {column} information")

        worksheet.write(row_iteration, col_iteration, summary_df[column].name, bold)
        worksheet.write(const_sum_dov_data_type_row, col_iteration, summary_df.loc['Data Type'][column])

        worksheet.write(const_sum_dov_count_row, col_iteration, summary_df.loc['count'][column])
        worksheet.write(const_sum_dov_num_nan_row, col_iteration, summary_df.loc['total_null'][column])
        worksheet.write(const_sum_dov_nan_perc_row, col_iteration, summary_df.loc['total_null_perc'][column])

        worksheet.write(const_sum_dov_mean_row, col_iteration, summary_df.loc['mean'][column])
        worksheet.write(const_sum_dov_median_row, col_iteration, summary_df.loc['median'][column])
        worksheet.write(const_sum_dov_std_row, col_iteration, summary_df.loc['std'][column])
        worksheet.write(const_sum_dov_var_row, col_iteration, summary_df.loc['var'][column])
        worksheet.write(const_sum_dov_range_row, col_iteration, summary_df.loc['range'][column])
        worksheet.write(const_sum_dov_0_prct_row, col_iteration, summary_df.loc['0%'][column])
        worksheet.write(const_sum_dov_25_prct_row, col_iteration, summary_df.loc['25%'][column])
        worksheet.write(const_sum_dov_50_prct_row, col_iteration, summary_df.loc['50%'][column])
        worksheet.write(const_sum_dov_75_prct_row, col_iteration, summary_df.loc['75%'][column])
        worksheet.write(const_sum_dov_100_prct_row, col_iteration, summary_df.loc['100%'][column])

        worksheet.write(row_data_header - 1, col_iteration, 'DOV', underline)
        worksheet.write(row_data_header - 1, col_iteration + 1, 'DistPrc', underline)

        const_data_type_continuous = 'continuous'
        const_data_type_categorical = 'categorical'
        const_data_type_discrete = 'discrete'

        var_type = const_data_type_continuous
        worksheet.write(const_sum_dov_cont_or_desc_row, col_iteration, const_data_type_continuous)

        unique_count_num = spark_df.select(column).distinct().count()
        is_numeric_col = is_spark_numeric_data_type(spark_df.schema.fields[spark_df.columns.index(column)])

        if unique_count_num > 500:
            if is_numeric_col:
                var_type = const_data_type_continuous
            else:
                var_type = const_data_type_categorical
        else:
            if unique_count_num< 100:
                if is_numeric_col:
                    var_type = const_data_type_discrete
                else:
                    var_type = const_data_type_categorical
            else:
                var_type = const_data_type_categorical

        worksheet.write(row_iteration + const_sum_dov_cont_or_desc_row, col_iteration, var_type)

        # Group by the category and count occurrences
        category_counts = spark_df.groupBy(column).count()

        # Calculate percentage for each category
        disb_df = category_counts.withColumn("distprc", (f.col("count") / spark_df.count()) * 100)\
            .select(f.col(column).alias("dov"), "distprc")\
            .orderBy("distprc")\
            .limit(1000)\
            .toPandas()

        if unique_count_num > 500:
            worksheet.write(row_data_header, col_iteration, '> 500 unq', italic)
            worksheet.write_column(row_data_header + 1, col_iteration, disb_df.loc[:, 'dov'].head(100))
            col_iteration += 1

            worksheet.write(row_data_header, col_iteration, '> 500 unq')
            worksheet.write_column(row_data_header + 1, col_iteration, disb_df.loc[:, 'distprc'].head(100))
            col_iteration += 1
        else:
            worksheet.write_column(row_data_header, col_iteration, disb_df.loc[:, 'dov'])
            col_iteration += 1

            worksheet.write(row_data_header, col_iteration, 'DistPrc')
            worksheet.write_column(row_data_header, col_iteration, disb_df.loc[:, 'distprc'])
            col_iteration += 1

        # cleanup
        del disb_df

    worksheet.freeze_panes(const_sum_dov_row_data_header, 1)

    print(f"{func_name}: sheet completed - DOV")


def add_sheet_summary_ordered(workbook: xlsxwriter.Workbook,
                              summary_df: pandas.DataFrame) -> None:
    # Add the summary stats in ordered fashion for easy filtering
    func_name = add_sheet_summary_ordered.__name__

    worksheet = workbook.add_worksheet('OrderSummaryStats')
    worksheet_add_df(input_workbook=workbook,
                     input_worksheet=worksheet,
                     input_sheet_name='OrderSummaryStats',
                     input_dataframe=summary_df.transpose(),
                     input_start_row=0,
                     input_start_col=0,
                     input_use_index=True)

    print(f"{func_name}: sheet completed - Summary Stats Ordered")


def add_sheet_correlation(workbook: xlsxwriter.Workbook,
                          df: pandas.DataFrame) -> None:
    # Correlation worksheet
    func_name = add_sheet_correlation.__name__

    worksheet = workbook.add_worksheet('Correlation')
    df_corr = df[df.select_dtypes(include='number').columns].corr().round(ROUND_PRECISION)

    worksheet_add_df(input_workbook=workbook,
                     input_worksheet=worksheet,
                     input_sheet_name='Correlation',
                     input_dataframe=df_corr,
                     input_start_row=0,
                     input_start_col=0,
                     input_use_index=True)

    format_high = workbook.add_format({'font_color': 'red'})
    format_low = workbook.add_format({'font_color': 'blue'})

    len_cols_df_corr = len(df_corr.columns) + 1
    len_rows_df_corr = len(df_corr.index) + 4
    cell_start = xl_rowcol_to_cell(3, 2)
    cell_end = xl_rowcol_to_cell(len(df_corr.index) + 2, len(df_corr.columns))
    worksheet.conditional_format(cell_start + ':' + cell_end, {'type': 'cell',
                                                               'criteria': '>=',
                                                               'value': 0.60,
                                                               'format': format_high})

    worksheet.conditional_format('B3:K12', {'type': 'cell',
                                            'criteria': '<',
                                            'value': -0.60,
                                            'format': format_low})

    print(f"{func_name}: sheet completed - Correlation")


def add_sheet_covariance(workbook: xlsxwriter.Workbook,
                         df: pandas.DataFrame) -> None:
    # Covariance worksheet
    func_name = add_sheet_covariance.__name__
    worksheet = workbook.add_worksheet('Co-Variance')
    worksheet_add_df(input_workbook=workbook,
                     input_worksheet=worksheet,
                     input_sheet_name='Co-Variance',
                     input_dataframe=df[df.select_dtypes(include='number').columns].cov().round(ROUND_PRECISION),
                     input_start_row=0,
                     input_start_col=0,
                     input_use_index=True)

    print(f"{func_name}: sheet completed - Covariance")


def add_sheet_samples_python(workbook: xlsxwriter.Workbook,
                             df: pandas.DataFrame) -> None:
    # Head / Tail samples worksheet
    func_name = add_sheet_samples_python.__name__

    worksheet = workbook.add_worksheet('150samples')
    worksheet_add_df(input_workbook=workbook,
                     input_worksheet=worksheet,
                     input_sheet_name='150samples (Top 75)',
                     input_dataframe=df.head(75),
                     input_start_row=0,
                     input_start_col=0,
                     input_use_index=True)

    worksheet_add_df(input_workbook=workbook,
                     input_worksheet=worksheet,
                     input_sheet_name='150samples (Tail 75)',
                     input_dataframe=df.tail(75),
                     input_start_row=80,
                     input_start_col=0,
                     input_use_index=True)

    print(f"{func_name}: sheet completed - 150 Head / Tail Samples")

def add_sheet_samples_spark(workbook: xlsxwriter.Workbook,
                            spark_df) -> None:
    # For spark - just take 150 samples to avoid a sort.
    func_name = add_sheet_samples_python.__name__

    worksheet = workbook.add_worksheet('150samples')
    worksheet_add_df(input_workbook=workbook,
                     input_worksheet=worksheet,
                     input_sheet_name='150samples',
                     input_dataframe=spark_df.limit(150).toPandas(),
                     input_start_row=0,
                     input_start_col=0,
                     input_use_index=True)

    print(f"{func_name}: sheet completed - 150 Samples")
