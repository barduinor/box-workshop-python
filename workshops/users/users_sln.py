"""Box Users workshop"""
import logging

from boxsdk import Client, BoxAPIException
from boxsdk.object.item import Item
from boxsdk.object.folder import Folder
from boxsdk.object.file import File
from boxsdk.object.user import User

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def get_user_by_id(client: Client, user_id: str) -> User:
    return client.user(user_id).get()


def create_user(client: Client, name: str, login: str) -> User:
    return client.create_user(name, login)


def main():
    """
    Simple script to demonstrate how to use the Box SDK
    with oAuth2 authentication
    """
    client = get_client(conf)

    user = client.user().get()
    print(f"\nHello, {user.name}, ({user.login}) [{user.id}]")

    me = get_user_by_id(client, "me")
    print(f"\nHello there, {user.name}, ({user.login}) [{user.id}]")

    # # Create a new user
    # second_user = create_user(client, "Second User", login=None)

    # users = client.users(user_type="all")
    # for user in users:
    #     print(f"{user.name} (User ID: {user.id})")


if __name__ == "__main__":
    main()
