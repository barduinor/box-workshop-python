""" Searching Box exercises"""
import logging
from typing import Iterable

from boxsdk.object.item import Item
from boxsdk.object.folder import Folder

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def print_box_item(box_item: Item):
    """Basic print of a Box Item attributes"""
    print(f"Type: {box_item.type} ID: {box_item.id} Name: {box_item.name}")


def print_search_results(items: Iterable["Item"]):
    """Print search results"""
    print("--- Search Results ---")
    for item in items:
        print_box_item(item)
    print("--- End Search Results ---")


def simple_search(
    query: str,
    content_types: Iterable[str] = None,
    result_type: str = None,
    ancestor_folders: Iterable["Folder"] = None,
) -> Iterable["Item"]:
    """Search by query in any Box content"""

    return client.search().query(
        query=query,
        content_types=content_types,
        result_type=result_type,
        ancestor_folders=ancestor_folders,
    )


if __name__ == "__main__":
    client = get_client(conf)

    # # Simple Search
    # search_results = simple_search("apple")
    # print_search_results(search_results)

    # # Expanded Search
    # search_results = simple_search("apple banana")
    # print_search_results(search_results)

    # # "Exact" Search
    # search_results = simple_search('"apple banana"')
    # print_search_results(search_results)

    # # Operators Search
    # search_results = simple_search("apple NOT banana")
    # print_search_results(search_results)

    # # Operators Search
    # search_results = simple_search("apple AND pineapple")
    # print_search_results(search_results)

    # # Operators Search
    # search_results = simple_search("pineapple OR banana")
    # print_search_results(search_results)

    # # More Searches
    # search_results = simple_search("ananas")
    # print_search_results(search_results)

    # # Search only in name
    # search_results = simple_search(
    #     "ananas",
    #     content_types=[
    #         "name",
    #     ],
    # )
    # print_search_results(search_results)

    # # Search in name and description
    # search_results = simple_search(
    #     "ananas",
    #     content_types=[
    #         "name",
    #         "description",
    #     ],
    # )
    # print_search_results(search_results)

    # # Search for folders only
    # search_results = simple_search("apple", result_type="folder")
    # print_search_results(search_results)

    # # Search banana
    # search_results = simple_search("banana")

    # print("--- Search Results ---")
    # for item in search_results:
    #     print(f"Type: {item.type} ID: {item.id} Name: {item.name} Folder: {item.parent.name}")
    # print("--- End Search Results ---")

    # # Ancestor Search
    # folder_apple_banana = client.folder("231320711952")
    # folder_banana_apple = client.folder("231320108594")
    # search_results = simple_search(
    #     "banana",
    #     ancestor_folders=[folder_apple_banana, folder_banana_apple],
    #     result_type="file",
    # )

    # print("--- Search Results ---")
    # for item in search_results:
    #     print(f"Type: {item.type} ID: {item.id} Name: {item.name} Folder: {item.parent.name}")
    # print("--- End Search Results ---")
