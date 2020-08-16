import os

from decouple import config
from google.cloud import storage

from Screw_Youtube.settings import GS_BUCKET_NAME


def get_client():
    return storage.Client.from_service_account_json(config('GS_CREDENTIALS'))


def upload_file(filename, file_path, remote_location):
    """
    This function uploads the file to server.
    :param filename: Name of the file.
    :param file_path: Path to the file.
    :param remote_location: Location of where the uploaded file will be stored on the server.
    """
    storage_client = get_client()
    bucket = storage_client.bucket(GS_BUCKET_NAME)
    blob = bucket.blob(os.path.join(remote_location, filename))
    blob.upload_from_filename(file_path)
    return blob.public_url
