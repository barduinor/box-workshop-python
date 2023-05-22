""" Searching Box exercises"""
import logging
from typing import Iterable

from boxsdk.object.item import Item

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def print_box_item(box_item: Item):
    """Basic print of a Box Item attributes"""
    print(f"Type: {box_item.type} ID: {box_item.id} Name: {box_item.name}, ")


def print_search_results(items: Iterable["Item"]):
    """Print search results"""
    print("--- Search Results ---")
    for item in items:
        print_box_item(item)
    print("--- End Search Results ---")


def simple_search(query: str) -> Iterable["Item"]:
    """Search by query in any Box content"""

    return client.search().query(query=query)


if __name__ == "__main__":
    client = get_client(conf)

    # Simple Search
    search_results = simple_search("box")
    print_search_results(search_results)
