import numpy as np
import pandas
import pandas as pd


ROUND_PRECISION = 4
ROUND_PRECISION_2 = 2
ROUND_PRECISION_4 = 4


def generate_summary_stats(df: pandas.DataFrame):
    # Generate summary statistics for a dataframe

    running_df = pd.DataFrame()

    for column in df:
        col_metric = {
            "dtype": "",
            "count": "",
            "total_null": "",
            "total_null_perc": "",
            "mean": "",
            "median": "",
            "std": "",
            "var": "",
            "range": "",
            "0%": "",
            "25%": "",
            "50%": "",
            "75%": "",
            "100%": ""
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
            col_metric['count'] = np.round(df[column].count(), ROUND_PRECISION)
            col_metric['mean'] = np.round(df[column].mean(), ROUND_PRECISION)
            col_metric['median'] = np.round(df[column].median(), ROUND_PRECISION)
            col_metric['std'] = np.round(df[column].std(), ROUND_PRECISION)
            col_metric['var'] = np.round(df[column].var(), ROUND_PRECISION)
            col_metric['range'] = np.round(df[column].max() - df[column].min(), ROUND_PRECISION)
            col_metric['0%'] = np.round(df[column].quantile([0.0][0]), ROUND_PRECISION)
            col_metric['25%'] = np.round(df[column].quantile([0.25][0]), ROUND_PRECISION)
            col_metric['50%'] = np.round(df[column].quantile([0.50][0]), ROUND_PRECISION)
            col_metric['75%'] = np.round(df[column].quantile([0.75][0]), ROUND_PRECISION)
            col_metric['100%'] = np.round(df[column].quantile([1.0][0]), ROUND_PRECISION)

        temp_df = pd.DataFrame.from_dict(col_metric, orient='index', columns=[column])
        running_df = pd.concat([running_df, temp_df], axis=1).reindex(temp_df.index)

        # round
        running_df = running_df.round(ROUND_PRECISION)

        del temp_df

    return running_df