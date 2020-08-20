# noinspection PyPackageRequirements
import threading

from decouple import config
# noinspection PyPackageRequirements
from google.cloud import storage

from ScrewYoutube.settings import GS_BUCKET_NAME


def get_client():
    return storage.Client.from_service_account_json(config('GS_CREDENTIALS'))


def get_bucket(bucket_name=GS_BUCKET_NAME):
    storage_client = get_client()
    return storage_client.bucket(bucket_name)


def upload_file(filename, file_path, remote_location):
    """
    This function uploads the file to server.
    :param filename: Name of the file.
    :param file_path: Path to the file.
    :param remote_location: Location of where the uploaded file will be stored on the server.
    """
    bucket = get_bucket()
    blob = bucket.blob(remote_location + '/' + filename)
    blob.upload_from_filename(file_path)
    return blob.public_url


def delete_folder(folder_path):
    """
    This function deletes the folder from the server.
    """
    bucket = get_bucket()

    def _delete():
        blobs = bucket.list_blobs(prefix=folder_path)
        for blob in blobs:
            blob.delete()

    threading.Thread(target=_delete).start()
