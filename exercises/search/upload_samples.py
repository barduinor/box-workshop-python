"""Creates data for search exercises."""
import pathlib
import os
import logging

from boxsdk import Client
from boxsdk.object.folder import Folder
from boxsdk.object.file import File
from boxsdk.exception import BoxAPIException

logging.getLogger(__name__)


def create_box_folder(
    client: Client, folder_name: str, parent_folder: Folder
) -> Folder:
    """create a folder in box"""

    try:
        folder = parent_folder.create_subfolder(folder_name)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            folder_id = err.context_info["conflicts"][0]["id"]
            folder = client.folder(folder_id).get()
        else:
            raise err

    return folder


def folder_upload(
    client: Client,
    box_base_folder: Folder,
    local_folder_path: str,
) -> Folder:
    """upload a folder to box"""

    local_folder = pathlib.Path(local_folder_path)

    for item in local_folder.iterdir():
        if item.is_dir():
            new_box_folder = create_box_folder(client, item.name, box_base_folder)
            logging.info(" Folder %s", item.name)
            folder_upload(client, new_box_folder, item)
        else:
            file_upload(client, item, box_base_folder)
            logging.info(" \tUploaded %s", item.name)

    return box_base_folder


def file_upload(client: Client, file_path: str, folder: Folder) -> File:
    """upload a file to box"""

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    file = None
    try:
        folder.preflight_check(file_size, file_name)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            file_id = err.context_info["conflicts"]["id"]
            file = client.file(file_id).get()
        else:
            raise err

    if file is None:
        # upload new file
        file = folder.upload(file_path, file_name)
    else:
        # upload new version
        file = file.update_contents(file_path)

    if "pineapple" in file.name:
        file.update_info(data={"description": "aka ananas"})
    return file


def upload_content_sample(client: Client):
    """Uploads sample content to Box."""
    wks_folder = create_box_folder(client, "wokshops", client.folder("0"))

    search_folder = create_box_folder(client, "search", wks_folder)

    folder_upload(client, search_folder, "exercises/search/content_samples/")
