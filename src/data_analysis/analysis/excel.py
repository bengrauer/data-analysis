import os
import numpy as np
import pandas
import pandas as pd
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from io import BytesIO

from data_analysis.analysis.summary import generate_summary_stats, ROUND_PRECISION
from data_analysis.utility.file_path_ops import load_file


def workbook_get_physical_file(output_file_name) -> xlsxwriter.Workbook:
    # get the workbook for an os physical file
    return xlsxwriter.Workbook(output_file_name, {'nan_inf_to_errors': True})

def workbook_get_in_memory_file() -> tuple[BytesIO, xlsxwriter.Workbook]:
    # get in memory workbook
    workbook_bytes_io = BytesIO()
    return workbook_bytes_io, xlsxwriter.Workbook(workbook_bytes_io)

def workbook_write_in_memory_file_os(output_file_name: str, workbook_bytes_io):
    # write workbook from in memory to os file
    with open(output_file_name, 'wb') as f:
        f.write(workbook_bytes_io.getvalue())

def worksheet_add_df(input_workbook: xlsxwriter.Workbook,
                     input_worksheet: xlsxwriter.Workbook.worksheet_class,
                     input_sheet_name: str,
                     input_dataframe: pandas.DataFrame,
                     input_start_row: int = 0,
                     input_start_col: int = 0,
                     input_use_index: bool = False):
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


def add_sheet_summary_and_dov(workbook, df: pandas.DataFrame, summary_df: pandas.DataFrame):
    # Adds the main summary, domain of values and distribution percentages
    func_name = add_sheet_summary_and_dov.__name__

    worksheet = workbook.add_worksheet('DOV')

    bold = workbook.add_format({'bold': True})
    italic = workbook.add_format({'italic': True})
    underline = workbook.add_format({'underline': True})
    format_high = workbook.add_format({'font_color': 'red'})
    format_low = workbook.add_format({'font_color': 'blue'})

    offset_data_type = 1
    offset_count = 2
    offset_num_nan = 3
    offset_nan_perc = 4

    offset_mean = 5
    offset_median = 6
    offset_std = 7
    offset_var = 8
    offset_range = 9
    offset_0_prct = 10
    offset_25_prct = 11
    offset_50_prct = 12
    offset_75_prct = 13
    offset_100_prct = 14

    offset_cont_or_desc = 16
    offset_notes = 17

    offset_row_data_header = 19
    offset_row_freeze_row = 19

    col_iteration = 1
    row_iteration = 0
    row_data_header = offset_row_data_header

    worksheet.write(row_iteration, 0, 'Col Name', bold)
    worksheet.write(offset_data_type, 0, 'Data Type', bold)
    worksheet.write(offset_count, 0, 'count', bold)
    worksheet.write(offset_num_nan, 0, 'NaN', bold)
    worksheet.write(offset_nan_perc, 0, 'NaN %', bold)
    worksheet.write(offset_mean, 0, 'mean', bold)
    worksheet.write(offset_median, 0, 'median', bold)
    worksheet.write(offset_std, 0, 'std', bold)
    worksheet.write(offset_var, 0, 'var', bold)
    worksheet.write(offset_range, 0, 'range', bold)
    worksheet.write(offset_0_prct, 0, '0%', bold)
    worksheet.write(offset_25_prct, 0, '25%', bold)
    worksheet.write(offset_50_prct, 0, '50%', bold)
    worksheet.write(offset_75_prct, 0, '75%', bold)
    worksheet.write(offset_100_prct, 0, '100%', bold)

    worksheet.write(offset_cont_or_desc, 0, 'Var Type')
    worksheet.write(offset_notes, 0, 'Notes')

    for column in df:
        worksheet.write(row_iteration, col_iteration, df[column].name, bold)
        worksheet.write(offset_data_type, col_iteration, str(df[column].dtypes))

        worksheet.write(offset_count, col_iteration, summary_df.loc['count'][column])
        worksheet.write(offset_num_nan, col_iteration, summary_df.loc['total_null'][column])
        worksheet.write(offset_nan_perc, col_iteration, summary_df.loc['total_null_perc'][column])

        if np.issubdtype(df[column].dtype, np.number):
            worksheet.write(offset_mean, col_iteration, summary_df.loc['mean'][column])
            worksheet.write(offset_median, col_iteration, summary_df.loc['median'][column])
            worksheet.write(offset_std, col_iteration, summary_df.loc['std'][column])
            worksheet.write(offset_var, col_iteration, summary_df.loc['var'][column])
            worksheet.write(offset_range, col_iteration, summary_df.loc['range'][column])
            worksheet.write(offset_0_prct, col_iteration, summary_df.loc['0%'][column])
            worksheet.write(offset_25_prct, col_iteration, summary_df.loc['25%'][column])
            worksheet.write(offset_50_prct, col_iteration, summary_df.loc['50%'][column])
            worksheet.write(offset_75_prct, col_iteration, summary_df.loc['75%'][column])
            worksheet.write(offset_100_prct, col_iteration, summary_df.loc['100%'][column])

        worksheet.write(row_data_header - 1, col_iteration, 'DOV', underline)
        worksheet.write(row_data_header - 1, col_iteration + 1, 'DistPrc', underline)

        const_data_type_continuous = 'continuous'
        const_data_type_categorical = 'categorical'
        const_data_type_discrete = 'discrete'

        var_type = const_data_type_continuous
        worksheet.write(offset_cont_or_desc, col_iteration, const_data_type_continuous)

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

        worksheet.write(row_iteration + offset_cont_or_desc, col_iteration, var_type)

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

    worksheet.freeze_panes(offset_row_data_header, 1)

    print(f"{func_name}: sheet completed - DOV")


def add_sheet_summary_ordered(workbook, summary_df: pandas.DataFrame):
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


def add_sheet_correlation(workbook, df: pandas.DataFrame):
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


def add_sheet_covariance(workbook, df: pandas.DataFrame):
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


def add_sheet_samples(workbook, df: pandas.DataFrame):
    # Head / Tail samples worksheet
    func_name = add_sheet_samples.__name__

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


def generate_excel_workbook(input_file_name: str, output_file_name: str):
    # Main function to load the file and generate the excel workbook
    func_name = generate_excel_workbook.__name__

    df = load_file(input_file_name)
    workbook_bytes_io, workbook = workbook_get_in_memory_file()

    summary_df = generate_summary_stats(df)

    add_sheet_summary_and_dov(workbook, df, summary_df)
    add_sheet_summary_ordered(workbook, summary_df)
    add_sheet_correlation(workbook, df)
    add_sheet_covariance(workbook, df)
    add_sheet_samples(workbook, df)

    workbook.close()
    workbook_write_in_memory_file_os(output_file_name=output_file_name, workbook_bytes_io=workbook_bytes_io)

    print(f"{func_name}: excel workbook generated: {output_file_name}")