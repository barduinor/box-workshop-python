"""main.py"""

import logging
from utils.config import AppConfig

from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def main():
    """
    Simple script to demonstrate how to use the Box SDK
    with oAuth2 authentication
    """

    client = get_client(conf)

    user = client.user().get()
    user = client.user().get()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")


if __name__ == "__main__":
    main()
