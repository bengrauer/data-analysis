import os
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from azure.identity import ClientSecretCredential

from data_analysis.utility.run_settings import RunSettings

def get_blob_service_client_from_secrets(run_settings: RunSettings) -> BlobServiceClient:
    credential = ClientSecretCredential(tenant_id=run_settings.azure_tenant_id,
                                        client_id=run_settings.azure_client_id,
                                        client_secret=run_settings.azure_client_secret)

    blob_service_client = BlobServiceClient(account_url=run_settings.azure_account_url,
                                            credential=credential)

    return blob_service_client


def read_bytesio_in_chunks(data: bytes,
                           chunk_size: int):
    with BytesIO(data) as bio:
        while True:
            chunk = bio.read(chunk_size)
            if not chunk:
                break
            yield chunk


def upload_file_from_bytes_in_chunks(run_settings: RunSettings,
                                     file_bytes_io: BytesIO) -> None:
    try:
        blob_service_client = get_blob_service_client_from_secrets(run_settings=run_settings)

        blob_client = blob_service_client.get_blob_client(container=run_settings.azure_container_name,
                                                          blob=run_settings.azure_blob_file_name)

        # set pointer to the beginning of file
        file_bytes_io.seek(0)

        bytes_data = file_bytes_io.read()
        for chunk in read_bytesio_in_chunks(bytes_data, run_settings.file_chunk_size):
            blob_client.upload_blob(chunk, overwrite=True)

        print(f"File uploaded successfully to '{run_settings.azure_container_name}'.")
    except Exception as e:
        raise Exception(f"Error uploading file: {e}")
