"""upload sample content to box"""
import logging
from utils.config import AppConfig

from utils.box_client import get_client

from workshops.search.upload_samples import upload_content_sample

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


if __name__ == "__main__":
    client = get_client(conf)
    upload_content_sample(client)
