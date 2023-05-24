"""Box Folder workshop"""
import logging
from typing import Iterable

from boxsdk import Client, BoxAPIException
from boxsdk.object.item import Item
from boxsdk.object.folder import Folder

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def print_box_item(box_item: Item, level: int = 0):
    """Basic print of a Box Item attributes"""
    print(
        f"{'   ' * level}({box_item.id}) {box_item.name}{'/' if box_item.type == 'folder' else ''}"
    )


def print_box_items(box_items: Iterable["Item"]):
    """Print items"""
    print("--- Items ---")
    for box_item in box_items:
        print_box_item(box_item)
    print("-------------")


def get_folder_items(box_client: Client, box_folder_id: str = "0") -> Iterable["Item"]:
    """Get folder items"""
    folder = box_client.folder(folder_id=box_folder_id).get()
    return folder.get_items()


def print_folder_items_recursive(
    box_client: Client, folder: Folder, level: int = 0
) -> Iterable["Item"]:
    """Get folder items recursively"""
    print_box_item(folder, level)
    box_items = folder.get_items()
    for box_item in box_items:
        if box_item.type == "folder":
            print_folder_items_recursive(box_client, box_item, level + 1)
        else:
            print_box_item(box_item, level + 1)


def get_workshop_folder(box_client: Client) -> Folder:
    """Get workshop folder"""
    root = box_client.folder(folder_id="0").get()
    workshops_folder_list = [
        box_item
        for box_item in root.get_items()
        if box_item.name == "workshops" and box_item.type == "folder"
    ]
    if workshops_folder_list == []:
        raise ValueError("'Workshop' folder not found")

    folders_folder_list = [
        box_item
        for box_item in workshops_folder_list[0].get_items()
        if box_item.name == "folders" and box_item.type == "folder"
    ]
    if folders_folder_list == []:
        raise ValueError("'Folders' folder not found")

    return folders_folder_list[0]


def create_box_folder(
    box_client: Client, folder_name: str, parent_folder: Folder
) -> Folder:
    """create a folder in box"""

    try:
        folder = parent_folder.create_subfolder(folder_name)
    except BoxAPIException as box_err:
        if box_err.code == "item_name_in_use":
            box_folder_id = box_err.context_info["conflicts"][0]["id"]
            folder = box_client.folder(box_folder_id).get()
        else:
            raise box_err

    # logging.info("Folder %s with id: %s", folder.name, folder.id)
    return folder


if __name__ == "__main__":
    client = get_client(conf)

    # items = get_folder_items(client)
    # print_box_items(items)

    # root_folder = client.folder(folder_id="0").get()
    # print_folder_items_recursive(client, root_folder)

    wksp_folder = get_workshop_folder(client)

    my_documents = create_box_folder(client, "my_documents", wksp_folder)
    work = create_box_folder(client, "work", my_documents)

    downloads = create_box_folder(client, "downloads", wksp_folder)
    personal = create_box_folder(client, "personal", downloads)

    try:
        my_docs_personal = personal.copy(parent_folder=my_documents)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            folder_id = err.context_info["conflicts"]["id"]
            my_docs_personal = client.folder(folder_id).get()
        else:
            raise err

    downloads.update_info(
        data={
            "description": "This is where my donwloads go, remember to clean it once in a while"
        }
    )
    print(f"{downloads.type} {downloads.id} {downloads.name}")
    print(f"Description: {downloads.description}")

    tmp = create_box_folder(client, "tmp", downloads)
    tmp2 = create_box_folder(client, "tmp2", tmp)

    print("--- Before the delete ---")
    print_folder_items_recursive(client, downloads)
    print("---")

    try:
        tmp.delete(recursive=False)
    except BoxAPIException as err:
        if err.code == "folder_not_empty":
            print(f"Folder {tmp.name} is not empty, deleting recursively")
            try:
                tmp.delete()
            except BoxAPIException as err_l2:
                raise err_l2
        else:
            raise err

    print("--- After the delete ---")
    print_folder_items_recursive(client, downloads)
    print("---")

    print("Renaming personal download to games")
    games = personal.rename("games")
    print_folder_items_recursive(client, downloads)
    print("---")

    print("Deleting games")
    games.delete()
    print_folder_items_recursive(client, downloads)
    print("---")

    # print_folder_items_recursive(client, wksp_folder)
