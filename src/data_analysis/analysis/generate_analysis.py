# Author: Ben Grauer
# Created a python script that does some basic exploratory analysis / dov and exports to excel for easy viewing
# Designed for quick exploratory analysis of the data sets from Kaggle

# imports
import sys
import os
import numpy as np
import pandas as pd
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

from data_analysis.utility.file_path_ops import (check_is_directory,
                                   directory_exists,
                                   append_analysis_directory,
                                   load_file,
                                   check_is_file)

ROUND_PERCISION = 4
ROUND_PERCISION_2 = 2
ROUND_PERCISION_4 = 4

def generate_summary_stats(df):
    running_df = pd.DataFrame()

    for column in df:
        col_metric = {
            'dtype': '',
            'count': '',
            'total_null': '',
            'total_null_perc': '',
            'mean': '',
            'median': '',
            'std': '',
            'var': '',
            'range': '',
            '0%': '',
            '25%': '',
            '50%': '',
            '75%': '',
            '100%': ''
        }

        col_metric['dtype'] = str(df[column].dtype)
        col_metric['count'] = len(df[column])

        total_null = len(df[column]) - df[column].count()
        col_metric['total_null'] = total_null

        if total_null > 0:
            total_null_perc = str(round(((len(df) - df[column].count()) / len(df[column])) * 100, 0))
        else:
            total_null_perc = '0'
        col_metric['total_null_perc'] = total_null_perc

        if np.issubdtype(df[column].dtype, np.number):
            col_metric['count'] = np.round(df[column].count(), ROUND_PERCISION)
            col_metric['mean'] = np.round(df[column].mean(), ROUND_PERCISION)
            col_metric['median'] = np.round(df[column].median(), ROUND_PERCISION)
            col_metric['std'] = np.round(df[column].std(), ROUND_PERCISION)
            col_metric['var'] = np.round(df[column].var(), ROUND_PERCISION)
            col_metric['range'] = np.round(df[column].max() - df[column].min(), ROUND_PERCISION)
            col_metric['0%'] = np.round(df[column].quantile([0.0][0]), ROUND_PERCISION)
            col_metric['25%'] = np.round(df[column].quantile([0.25][0]), ROUND_PERCISION)
            col_metric['50%'] = np.round(df[column].quantile([0.50][0]), ROUND_PERCISION)
            col_metric['75%'] = np.round(df[column].quantile([0.75][0]), ROUND_PERCISION)
            col_metric['100%'] = np.round(df[column].quantile([1.0][0]), ROUND_PERCISION)

        temp_df = pd.DataFrame.from_dict(col_metric, orient='index', columns=[column])
        running_df = pd.concat([running_df, temp_df], axis=1).reindex(temp_df.index)

        # round
        running_df = running_df.round(ROUND_PERCISION)

    return running_df


def excel_add_df(input_workbook, input_worksheet, input_sheet_name, input_dataframe,
                 input_start_row=0, input_start_col=0, input_use_index=False):
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


def excel_addsheet_summary_and_dov(workbook, df, summary_df):
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

        disb_df = pd.DataFrame(df.groupby([column]).size() * 100 / len(df)).round(ROUND_PERCISION)
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
    print('excel sheet completed - DOV')


def excel_addsheet_summary_ordered(workbook, summary_df):
    worksheet = workbook.add_worksheet('OrderSummaryStats')
    excel_add_df(input_workbook=workbook, input_worksheet=worksheet, input_sheet_name='OrderSummaryStats',
                 input_dataframe=summary_df.transpose(), input_start_row=0, input_start_col=0, input_use_index=True)

    print('excel sheet completed - Summary Stats Ordered')


def excel_addsheet_correlation(workbook, df):
    worksheet = workbook.add_worksheet('Correlation')
    df_corr = df[df.select_dtypes(include='number').columns].corr().round(ROUND_PERCISION)

    excel_add_df(input_workbook=workbook, input_worksheet=worksheet, input_sheet_name='Correlation',
                 input_dataframe=df_corr, input_start_row=0, input_start_col=0, input_use_index=True)

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

    print('excel sheet completed - Correlation')


def excel_addsheet_covariance(workbook, df):
    worksheet = workbook.add_worksheet('Co-Variance')
    excel_add_df(input_workbook=workbook, input_worksheet=worksheet, input_sheet_name='Co-Variance',
                 input_dataframe=df[df.select_dtypes(include='number').columns].cov().round(ROUND_PERCISION), input_start_row=0, input_start_col=0, input_use_index=True)

    print('excel sheet completed - Covariance')


def excel_addsheet_samples(workbook, df):
    worksheet = workbook.add_worksheet('150samples')
    excel_add_df(input_workbook=workbook, input_worksheet=worksheet, input_sheet_name='150samples (Top 75)',
                 input_dataframe=df.head(75), input_start_row=0, input_start_col=0, input_use_index=True)

    excel_add_df(input_workbook=workbook, input_worksheet=worksheet, input_sheet_name='150samples (Tail 75)',
                 input_dataframe=df.tail(75), input_start_row=80, input_start_col=0, input_use_index=True)

    print('excel sheet completed - 150 Head / Tail Samples')


def generate_excel_workbook(input_file_name, output_file_name):
    df = load_file(input_file_name)
    workbook = xlsxwriter.Workbook(output_file_name, {'nan_inf_to_errors': True})

    summary_df = generate_summary_stats(df)

    excel_addsheet_summary_and_dov(workbook, df, summary_df)
    excel_addsheet_summary_ordered(workbook, summary_df)
    excel_addsheet_correlation(workbook, df)
    excel_addsheet_covariance(workbook, df)
    excel_addsheet_samples(workbook, df)

    workbook.close()
    print('excel workbook generated: ' + output_file_name)


def run_analysis_routine(file_or_directory, output_directory):
    directory_to_evaluate = ""

    if check_is_file(file_or_directory):
        is_file_to_analyze = True
        is_path_to_analyze = False
        file_to_evaluate = file_or_directory
    elif check_is_directory(file_or_directory):
        is_path_to_analyze = True
        is_file_to_analyze = False
        directory_to_evaluate = file_or_directory
    else:
        is_file_to_analyze = False
        is_path_to_analyze = False
        raise Exception(f"Error - Invalid file or path passed in.  {file_or_directory}")

    if not directory_exists(directory=output_directory, auto_create=True):
        raise Exception(f"Error - Invalid output directory passed in.  {output_directory}")

    if is_path_to_analyze:
        if not output_directory:
            output_directory = append_analysis_directory(directory_to_evaluate)

        for file_name in os.listdir(file_or_directory):
            if len(file_name) > 3 and file_name[-4:] == '.csv':
                print('input file: ' + directory_to_evaluate + file_name)
                output_file_name = os.path.join(output_directory, ('analysis_' + str(file_name)[:-4] + '_v2.xlsx'))
                print('file to generate: ' + output_file_name)
                generate_excel_workbook(directory_to_evaluate + file_name, output_file_name)

    elif is_file_to_analyze:
        file_name = os.path.basename(file_or_directory)
        input_directory = os.path.dirname(file_or_directory)
        if not output_directory:
            output_directory = append_analysis_directory(input_directory)
        output_file_name = os.path.join(output_directory, ('analysis_' + str(file_name)[:-4] + '_v2.xlsx'))
        print('file to generate: ' + output_file_name)
        generate_excel_workbook(file_or_directory, output_file_name)


# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         print('arg 1: ' + str(sys.argv[1]))
#         file_or_directory = sys.argv[1]
# 
#     file_or_directory = "/media/data/project/data/kg_RussiaHousing/train.csv"
#     run_analysis_routine(file_or_directory)