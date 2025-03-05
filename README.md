# data-analysis
Personal project used for data profiling, showing dov (domain of values) distributions, sample, data, etc.  Exports data to excel for 
analysis and notes.  Was Used as a starting point for Kaggle competitions to look at data and think about features.

Not open for PRs due to this being a personal project.

## Example Output
![Alt text](/docs/data_analysis_example_pic_dov.png)


## Installation
- Package Install
```bash
pip install git+https://github.com/bengrauer/data-analysis.git@main
```

## Usage
- Usage is now direct calls to the package.  This was done to accommodate spark/cloud scenarios.
- Cloud processing requires client/secret keys set in the os environment variables.  They can also be passed into
the RunSettings class if desired.
  - AZURE:
    - TENANT_ID, CLIENT_ID, CLIENT_SECRET
  - AWS
    - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
#
### Running locally with a csv directory
```python
from data_analysis.analysis import generate_analysis
from data_analysis.utility.run_settings import RunSettings, RunType, EnvRun

run_settings = RunSettings(
    run_type=RunType.PYTHON,
    env_run=EnvRun.LOCAL,
    input_dir="/input_dir/",
    output_dir="/output_dir/"
)

generate_analysis.run_analysis_routine_local_csv(run_settings=run_settings)
```
#
### Running in the cloud with pyspark
- Running in the cloud requires you to instantiate your own spark instance, pass in your own dataframe.
Because dataframes can vary in how they are read in, this avoids complications within the framework. 
It is also advised to cache the dataframe before passing in for processing to avoid un-necessary disk retrievals.
- It would also be advised to increase the driver memory (spark.driver.memory) to allow the processes in python to run efficiently.
The processing logic converts several aggregate spark dataframes to pandas before writing to excel.  In addition, the excel workbook is
written in memory before uploaded and saved to the object stores.  This helps skip any need for temporary disk writing.
- The cloud processing does not include the correlation or co-variance sheets at this time.
####
- Azure example
```python
import os
from data_analysis.analysis.generate_analysis import run_analysis_cloud_spark
from data_analysis.utility.run_settings import RunSettings, RunType, EnvRun

os.environ["TENANT_ID"] = "xxxxx"
os.environ["CLIENT_ID"] = "xxxxx"
os.environ["CLIENT_SECRET"] = "xxxxx"

# Here you will have to instantiate your own spark application and read in your own dataframe.
spark, spark_df = create_spark_session_and_load_dataframe()

# set run settings
run_settings = RunSettings(run_type=RunType.SPARK,
                           env_run=EnvRun.AZURE,
                           azure_account_url = "https://storageaccount.blob.core.windows.net",
                           azure_container_name = "container-name",
                           azure_blob_file_name ="folder/data_analysis.xlsx")

# load os env vars + validate azure components
run_settings\
        .load_azure_credentials_from_os_env_vars()\
        .validate_azure_components()

run_analysis_cloud_spark(run_settings=run_settings, spark=spark, spark_df=spark_df)

```

####
- AWS example
```python
import os
from data_analysis.analysis.generate_analysis import run_analysis_cloud_spark
from data_analysis.utility.run_settings import RunSettings, RunType, EnvRun

os.environ["AWS_ACCESS_KEY_ID"] = "xxxxx"
os.environ["AWS_SECRET_ACCESS_KEY"] = "xxxxx"

# Here you will have to instantiate your own spark application and read in your own dataframe.
spark, spark_df = create_spark_session_and_load_dataframe()

# set run settings
run_settings = RunSettings(run_type=RunType.SPARK,
                           env_run=EnvRun.AWS,
                           aws_bucket_name = "aws-bucket-name",
                           aws_object_file_name ="folder/data_analysis.xlsx")

# load os env vars + validate azure components
run_settings\
    .load_azure_credentials_from_os_env_vars()\
    .validate_aws_components()

run_analysis_cloud_spark(run_settings=run_settings, spark=spark, spark_df=spark_df)

```

