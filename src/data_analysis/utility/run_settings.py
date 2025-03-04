from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional
from enum import StrEnum

from data_analysis.utility.local_file_ops import directory_exists


class RunType(StrEnum):
    PYTHON = "python"
    SPARK = "spark"


class EnvRun(StrEnum):
    AWS = "aws"
    AZURE = "azure"
    LOCAL = "local"


class RunSettings(BaseSettings):
    run_type: str
    env_run: str
    input_dir: Optional[str] = ""
    output_dir: Optional[str] = ""
    output_file_name: Optional[str] = ""

    azure_tenant_id: Optional[str] = ""
    azure_client_id: Optional[str] = ""
    azure_client_secret: Optional[str] = ""

    azure_account_url: Optional[str] = ""
    azure_container_name: Optional[str] = ""
    azure_blob_file_name: Optional[str] = ""

    aws_access_key_id: Optional[str] = ""
    aws_secret_access_key: Optional[str] = ""

    aws_bucket_name: Optional[str] = ""
    aws_object_file_name: Optional[str] = ""
    file_chunk_size: Optional[int] = 4 * 1024 * 1024

    def model_post_init(self, __context):
        if self.run_type != RunType.SPARK:
            if self.env_run == EnvRun.LOCAL:
                if not directory_exists(directory=self.output_dir, auto_create=True):
                    raise Exception(f"Error - Invalid input directory passed in.  {self.input_dir}")

        if self.run_type != RunType.SPARK:
            if self.env_run == EnvRun.LOCAL:
                if not directory_exists(directory=self.output_dir, auto_create=True):
                    raise Exception(f"Error - Invalid output directory passed in.  {self.output_dir}")


    def load_azure_credentials_from_os_env_vars(self):
        import os
        self.azure_tenant_id = os.getenv("TENANT_ID", "")
        self.azure_client_id = os.getenv("CLIENT_ID", "")
        self.azure_client_secret = os.getenv("CLIENT_SECRET", "")
        return self

    def load_aws_credentials_from_os_env_vars(self):
        import os
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "")
        if not self.aws_access_key_id:
            raise Exception("'AWS_ACCESS_KEY_ID' not found in OS environment variables.")
        if not self.aws_secret_access_key:
            raise Exception("'AWS_SECRET_ACCESS_KEY' not found in OS environment variables.")
        return self

    def validate_azure_components(self):

        # secrets
        if not self.azure_tenant_id:
            raise Exception("'AZURE_TENANT_ID' not found in OS environment variables.")
        if not self.azure_client_id:
            raise Exception("'AZURE_CLIENT_ID' not found in OS environment variables.")
        if not self.azure_client_secret:
            raise Exception("'AZURE_SECRET' not found in OS environment variables.")

        if not self.azure_account_url:
            raise Exception("'azure_account_url' must be populated.")
        if not self.azure_container_name:
            raise Exception("'azure_container_name' must be populated.")
        if not self.azure_blob_file_name:
            raise Exception("'azure_blob_name' must be populated.")

        if self.azure_account_url:
            if "abfss:" in self.azure_account_url:
                raise Exception("please ensure 'azure_account_url' contains https prefix.  "
                                "Application cannot upload file output with abfss protocol.'")
            if "https:" not in self.azure_account_url:
                raise Exception("please ensure 'azure_account_url' contains https prefix.'")

    def validate_aws_components(self):
        if not self.aws_access_key_id:
            raise Exception("'AWS_ACCESS_KEY_ID' not found in OS environment variables.")
        if not self.aws_secret_access_key:
            raise Exception("'AWS_SECRET_ACCESS_KEY' not found in OS environment variables.")

        if not self.aws_bucket_name:
            raise Exception("'aws_bucket_name' must be populated.")
        if not self.aws_object_file_name:
            raise Exception("'aws_object_name' must be populated.")


