"""create sample content to box"""
import logging
from utils.config import AppConfig

from utils.box_client import get_client

from workshops.shared_links.create_samples import create_samples

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


if __name__ == "__main__":
    client = get_client(conf)
    create_samples(client)
