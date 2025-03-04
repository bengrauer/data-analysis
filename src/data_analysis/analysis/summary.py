import numpy as np
import pandas
import pandas as pd

ROUND_PRECISION = 4
ROUND_PRECISION_2 = 2
ROUND_PRECISION_4 = 4

def is_spark_numeric_data_type(col):
    from pyspark.sql.types import ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType
    if (isinstance(col.dataType, ByteType) or
            isinstance(col.dataType, ShortType) or
            isinstance(col.dataType, IntegerType) or
            isinstance(col.dataType, LongType) or
            isinstance(col.dataType, FloatType) or
            isinstance(col.dataType, DoubleType) or
            isinstance(col.dataType, DecimalType)):
        return True
    else:
        return False


def generate_summary_stats_spark(spark, df):
    from pyspark.sql import functions as f
    from pyspark.sql.functions import concat_ws
    from pyspark.sql.functions import expr

    func_name = generate_summary_stats_spark.__name__
    print(f"{func_name}: generating summary stats for spark.")

    if not df.is_cached:
        print(f"{func_name}: WARN! dataframe is not cached.  Caching will help speed up processing.")

    # Get column counts using list comprehension
    col_names = [col for col in df.columns]
    col_names_df = spark.createDataFrame(data=col_names, schema="STRING").withColumnRenamed("value", "Col Name")

    numeric_columns = [col.name for col in df.schema if is_spark_numeric_data_type(col)]

    data_types_list = []
    for x in df.schema:
        data_types_list.append(str(x.dataType).strip("()"))
    dtypes_df = spark.createDataFrame([tuple(data_types_list)], [x for x in df.schema.names])
    dtypes_df = dtypes_df.withColumnRenamed("value","Data Type")
    dtypes_df = dtypes_df.select(f.lit("Data Type").alias("metric"), "*")

    # count
    count_df = df.agg(*[f.count(c).alias(c) for c in df.columns])
    count_df = count_df.select(f.lit("count").alias("metric"), "*")

    # total_null
    total_null_df = df.agg(*[f.count(f.when(f.isnull(c), c)).alias(c) for c in df.columns])
    total_null_df = total_null_df.select(f.lit("total_null").alias("metric"), "*")

    # total null perc
    df_union_pd = count_df.union(total_null_df).toPandas().set_index("metric").transpose()
    df_union_pd['null %'] = (df_union_pd['total_null'] / df_union_pd['count']) * 100
    df_union_final = df_union_pd.transpose().loc[['null %']]
    null_perc_df = spark.createDataFrame(df_union_final)
    null_perc_df = null_perc_df.select(f.lit("total_null_perc").alias("metric"), "*")

    # mean
    mean_df = df.agg(*[f.round(f.mean(c), ROUND_PRECISION).alias(c) for c in numeric_columns])
    mean_df = mean_df.select(f.lit("mean").alias("metric"), "*")

    # median - has to be converted from string.
    df_median = df.agg(*[f.concat_ws(",", f.percentile_approx(c, [0.5])).alias(c) for c in numeric_columns])
    df_median = df_median.select(f.lit("median").alias("metric"), "*")

    # std
    std_df = df.agg(*[f.round(f.std(c), ROUND_PRECISION).alias(c) for c in numeric_columns])
    std_df = std_df.select(f.lit("std").alias("metric"), "*")

    # var
    var_df = df.agg(*[f.round(f.variance(c), ROUND_PRECISION).alias(c) for c in numeric_columns])
    var_df = var_df.select(f.lit("var").alias("metric"), "*")

    # range
    range_df = df.agg(*[(f.max(c) - f.min(c)).alias(c) for c in numeric_columns])
    range_df = range_df.select(f.lit("range").alias("metric"), "*")

    # 0%
    zero_dist_df = df.agg(*[f.concat_ws(",", f.percentile_approx(c, [0.0])).alias(c) for c in numeric_columns])
    zero_dist_df = zero_dist_df.select(f.lit("0%").alias("metric"), "*")

    # 25%
    twenty_five_dist_df = df.agg(*[f.concat_ws(",", f.percentile_approx(c, [0.25])).alias(c) for c in numeric_columns])
    twenty_five_dist_df = twenty_five_dist_df.select(f.lit("25%").alias("metric"), "*")

    # 50%
    fifty_dist_df = df.agg(*[f.concat_ws(",", f.percentile_approx(c, [0.50])).alias(c) for c in numeric_columns])
    fifty_dist_df = fifty_dist_df.select(f.lit("50%").alias("metric"), "*")

    # 75%
    seventy_five_dist_df = df.agg(*[f.concat_ws(",", f.percentile_approx(c, [0.75])).alias(c) for c in numeric_columns])
    seventy_five_dist_df = seventy_five_dist_df.select(f.lit("75%").alias("metric"), "*")

    # 100%
    one_hundred_dist_df = df.agg(*[f.concat_ws(",", f.percentile_approx(c, [1.0])).alias(c) for c in numeric_columns])
    one_hundred_dist_df = one_hundred_dist_df.select(f.lit("100%").alias("metric"), "*")

    # union all metrics.
    full_df = (dtypes_df
        .unionByName(count_df, allowMissingColumns=True)
        .unionByName(total_null_df, allowMissingColumns=True)
        .unionByName(null_perc_df, allowMissingColumns=True)
        .unionByName(mean_df, allowMissingColumns=True)
        .unionByName(df_median, allowMissingColumns=True)
        .unionByName(std_df, allowMissingColumns=True)
        .unionByName(var_df, allowMissingColumns=True)
        .unionByName(range_df, allowMissingColumns=True)
        .unionByName(zero_dist_df, allowMissingColumns=True)
        .unionByName(twenty_five_dist_df, allowMissingColumns=True)
        .unionByName(fifty_dist_df, allowMissingColumns=True)
        .unionByName(seventy_five_dist_df, allowMissingColumns=True)
        .unionByName(one_hundred_dist_df, allowMissingColumns=True))


    full_pd_df = full_df.toPandas()

    return full_pd_df



def generate_summary_stats_python(df: pandas.DataFrame):
    # Generate summary statistics for a dataframe

    running_df = pd.DataFrame()

    func_name = generate_summary_stats_python.__name__
    print(f"{func_name}: generating summary stats for python.")

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