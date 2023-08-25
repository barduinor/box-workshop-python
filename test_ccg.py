"""main.py"""

import logging
from utils.config import AppConfig

from utils.box_client import get_ccg_enterprise_client, get_ccg_user_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def main():
    """
    Simple script to demonstrate how to use the Box SDK
    with CCG authentication
    """

    client_enterprise = get_ccg_enterprise_client(conf)

    service_user = client_enterprise.user().get()
    print(f"\nHello, I'm {service_user.name} ({service_user.login}) [{service_user.id}]")

    client_user = get_ccg_user_client(conf)
    user = client_user.user().get()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")


if __name__ == "__main__":
    main()
