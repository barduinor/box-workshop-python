"""Creates data for search exercises."""
import pathlib
import os
import logging

from boxsdk import Client
from boxsdk.object.folder import Folder
from boxsdk.object.file import File
from boxsdk.exception import BoxAPIException

logging.getLogger(__name__)
