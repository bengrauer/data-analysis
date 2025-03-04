import pytest
from src.data_analysis.utility.run_settings import RunSettings, RunType, EnvRun


def test_run_settings_pass():
    assert RunSettings(run_type=RunType.PYTHON,
                       env_run=EnvRun.LOCAL,
                       input_dir="../data/input/",
                       output_dir="../data/output/")

def test_run_settings_fail():
    # run_type
    with pytest.raises(ValueError) as exc_info:
        RunSettings(run_type="",env_run="local",input_dir="../data/input/",output_dir="../data/output/")
    assert 'run_type' in str(exc_info.value)
    # env_run
    with pytest.raises(ValueError) as exc_info:
        RunSettings(run_type="python",env_run="",input_dir="../data/input/",output_dir="../data/output/")
    assert 'env_run' in str(exc_info.value)


def test_load_azure_credentials_from_os_env_vars_pass():
    import os
    os.environ["TENANT_ID"] = "xxx"
    os.environ["CLIENT_ID"] = "xxx"
    os.environ["CLIENT_SECRET"] = "xxx"

    run_settings = RunSettings(run_type=RunType.PYTHON,
                               env_run=EnvRun.AZURE,
                               azure_account_url="https://xxx.blob.core.windows.net",
                               azure_container_name="azure_container",
                               azure_blob_file_name="analysis.xlsx")
    run_settings.load_azure_credentials_from_os_env_vars()
    run_settings.validate_azure_components()
    assert True

def test_load_aws_credentials_from_os_env_vars_pass():
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = "xxx"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "xxx"

    run_settings = RunSettings(run_type=RunType.PYTHON,
                               env_run=EnvRun.AWS,
                               aws_bucket_name="aws-bucket-name",
                               aws_object_file_name="analysis.xlsx")
    run_settings.load_aws_credentials_from_os_env_vars()
    run_settings.validate_aws_components()
    assert True