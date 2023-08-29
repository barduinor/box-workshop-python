"""Box Shared links"""

from enum import Enum
import logging
from boxsdk import Client

from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.object.item import Item

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()

SHARED_LINKS_ROOT = "223783108378"
SAMPLE_FILE = "1293174201535"


class SharedLinkAccess(str, Enum):
    OPEN = "open"
    COMPANY = "company"
    COLLABORATORS = "collaborators"


def file_shared_link(
    file: File,
    access: SharedLinkAccess,
    allow_download: bool = None,
    allow_preview: bool = None,
    allow_edit: bool = None,
) -> str:
    return file.get_shared_link(
        access=access.value, allow_download=allow_download, allow_preview=allow_preview, allow_edit=allow_edit
    )


def folder_shared_link(
    folder: Folder,
    access: SharedLinkAccess,
    allow_download: bool = None,
    allow_preview: bool = None,
) -> str:
    return folder.get_shared_link(access=access.value, allow_download=allow_download, allow_preview=allow_preview)


def item_from_shared_link(client: Client, url: str, password: str = None) -> Item:
    return client.get_shared_item(url, password=password)


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    client = get_client(conf)

    user = client.user().get()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    file = client.file(SAMPLE_FILE).get()
    shared_link_file = file_shared_link(file, SharedLinkAccess.OPEN)
    print(f"\nShared link for {file.name}: {shared_link_file}")

    shared_link_view = file_shared_link(
        file, SharedLinkAccess.OPEN, allow_download=False, allow_preview=True, allow_edit=False
    )
    print(f"\nShared link for {file.name}: {shared_link_view}")

    folder = client.folder(SHARED_LINKS_ROOT).get()
    shared_link_folder = folder_shared_link(folder, SharedLinkAccess.OPEN)
    print(f"\nShared link for {folder.name}: {shared_link_folder}")

    url = file.get_shared_link_download_url(access=SharedLinkAccess.OPEN.value)
    print(f"\nDownload URL for {file.name}: {url}")

    item_a = item_from_shared_link(client, shared_link_file)
    print(f"\nItem from shared link: {item_a.name} is a {item_a.type} ({item_a.id})")

    item_b = item_from_shared_link(client, shared_link_folder)
    print(f"\nItem from shared link: {item_b.name} is a {item_b.type} ({item_b.id})")


if __name__ == "__main__":
    main()
