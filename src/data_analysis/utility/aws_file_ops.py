import io

from data_analysis.utility.run_settings import RunSettings

def upload_file_from_bytes(run_settings: RunSettings,
                           file_bytes_io: io.BytesIO) -> None:
    import boto3
    from boto3.s3.transfer import TransferConfig

    config = TransferConfig(multipart_chunksize=run_settings.file_chunk_size)
    s3_client = boto3.client('s3')

    try:
        s3client = boto3.client(
            's3',
            aws_access_key_id=run_settings.aws_access_key_id,
            aws_secret_access_key=run_settings.aws_access_key_id
        )

        # set pointer to the beginning of file
        file_bytes_io.seek(0)

        s3_client.upload_fileobj(file_bytes_io,
                                 run_settings.aws_bucket_name,
                                 run_settings.aws_object_file_name,
                                 Config=config)

        print(f"Upload to '{run_settings.aws_bucket_name}/{run_settings.aws_object_file_name}' successfully.")
    except Exception as e:
        raise Exception(f"Error uploading: {e}")


