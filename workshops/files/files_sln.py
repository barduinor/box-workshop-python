"""Box Files workshop"""
import logging
import os
from typing import Iterable

from boxsdk import Client, BoxAPIException
from boxsdk.object.item import Item
from boxsdk.object.folder import Folder
from boxsdk.object.file import File

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()
FILES_ROOT = "209588945595"


def upload_file(box_client: Client, box_folder: Folder, path_to_file: str) -> File:
    """Upload a file to a Box folder"""

    file_size = os.path.getsize(path_to_file)
    file_name = os.path.basename(path_to_file)

    try:
        box_folder.preflight_check(file_size, file_name)
        box_file = box_folder.upload(path_to_file)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            logging.warning("File already exists, updating contents")
            box_file_id = err.context_info["conflicts"]["id"]
            box_file = box_client.file(file_id=box_file_id).get()
            try:
                box_file.update_contents(path_to_file)
            except BoxAPIException as err2:
                logging.error("Failed to update %s: %s", box_file.name, err2)
                raise err2
        else:
            raise err

    return box_file


def download_file(box_file: File, local_path_to_file: str):
    """Download a file from Box"""

    with open(local_path_to_file, "wb") as file_stream:
        box_file.download_to(file_stream)


def download_zip(
    box_client: Client, local_path_to_zip: str, box_items: Iterable["Item"]
):
    """Download a zip file from Box"""
    file_name = os.path.basename(local_path_to_zip)
    with open(local_path_to_zip, "wb") as file_stream:
        box_client.download_zip(file_name, box_items, file_stream)


if __name__ == "__main__":
    client = get_client(conf)

    files_root = client.folder(folder_id=FILES_ROOT).get()

    sample_file = upload_file(
        client, files_root, "workshops/files/content_samples/sample_file.txt"
    )
    # print(f"Uploaded {sample_file.name} to {files_root.name}")

    # download_file(sample_file, "./sample_file_downloaded.txt")

    # for local_file in os.listdir("./"):
    #     if local_file.endswith(".txt"):
    #         print(local_file)

    user_root = client.folder(folder_id="0").get()

    items = []
    for item in user_root.get_items():
        items.append(item)

    print("Downloading zip")
    download_zip(client, "./sample_zip_downloaded.zip", items)

    for local_file in os.listdir("./"):
        if local_file.endswith(".zip"):
            print(local_file)
