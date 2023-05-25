# Files
File objects represent individual files in Box. They can be used to download a file's contents, upload new versions, and perform other common file operations (move, copy, delete, etc.).


## Concepts



## Files API
References to our documentation:
* [SDK Files](https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md)
* [API Folder Guide](https://developer.box.com/guides/files/)
* [API Reference](https://developer.box.com/reference/resources/file/)


# Exercises
## Setup
Create a `files_init.py` file on the root of the project and execute the following code:
```python
"""create sample content to box"""
import logging
from utils.config import AppConfig

from utils.box_client import get_client

from workshops.files.create_samples import create_samples

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


if __name__ == "__main__":
    client = get_client(conf)
    create_samples(client)
```
Result:
```
INFO:root:Folder workshops with id: 209408240392
INFO:root:Folder files with id: 209588945595
```
Grab the id of the `files` folder you'll need it later
Open your Box account and verify that the following content was uploaded:
```
- All Files
    - workshops
        -files
```


Next, create a `files.py` file on the root of the project that you will use to write your code.
Create a global constant named `FILES_ROOT` and make it equal to the id of the `files` folder.

```python
"""Box Files workshop"""
import logging
import os
from typing import Iterable

from boxsdk import Client, BoxAPIException
from boxsdk.object.item import Item
from boxsdk.object.folder import Folder
from boxsdk.object.file import File

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()
FILES_ROOT = "The id of the files folder"

if __name__ == "__main__":
    client = get_client(conf)

```

## New file upload
Create a method named `upload_file` that receives a `client` and a `file_path` and uploads the file to a specific folder.

```python
def upload_file(box_folder: Folder, path_to_file: str) -> File:
    """Upload a file to a Box folder"""
    return box_folder.upload(path_to_file)
```
Then upload the `workshops/files/content_samples/sample_file.txt` file to the `files` folder.
```python
if __name__ == "__main__":
    client = get_client(conf)

    files_root = client.folder(folder_id=FILES_ROOT).get()
    sample_file = upload_file(
        files_root, "workshops/files/content_samples/sample_file.txt"
    )
    print(f"Uploaded {sample_file.name} to {files_root.name}")
```
Should result in something similar to:
```
Uploaded sample_file.txt to files
```
## New file version upload
Files in Box have versions, you can upload a new version of a file by using the `upload` method of the file object.
Modify the `upload_file` method to upload a new file or a new version depending if the file exists or not.

```python
def upload_file(box_client:Client, box_folder: Folder, path_to_file: str) -> File:
    """Upload a file to a Box folder"""
    try:
        box_file = box_folder.upload(path_to_file)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            logging.warning("File already exists, updating contents")
            box_file_id = err.context_info["conflicts"]["id"]
            box_file = box_client.file(file_id=box_file_id).get()
            try:
                box_file.update_contents(path_to_file)
            except BoxAPIException as err2:
                logging.error("Failed to update %s: %s", box_file.name, err2)
                raise err2
        else:
            raise err
    return box_file
```
Then upload the `workshops/files/content_samples/sample_file.txt` file to the `files` folder.
```python

    files_root = client.folder(folder_id=FILES_ROOT).get()

    sample_file = upload_file(
        client, files_root, "workshops/files/content_samples/sample_file.txt"
    )
    print(f"Uploaded {sample_file.name} to {files_root.name}")
```
Should result in something similar to:
```
WARNING:root:File already exists, updating contents
Uploaded sample_file.txt to files
```

## Prefiligth check
There is another option to check if a file can be accepted by box before uploading it.
It typically checks for file name duplication and file size, in case you have exceeded your quota.
Modify the `upload_file` method to use the `preflight_check` method of the folder object:

```python
def upload_file(box_client: Client, box_folder: Folder, path_to_file: str) -> File:
    """Upload a file to a Box folder"""

    file_size = os.path.getsize(path_to_file)
    file_name = os.path.basename(path_to_file)

    try:
        box_folder.preflight_check(file_size, file_name)
        box_file = box_folder.upload(path_to_file)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            logging.warning("File already exists, updating contents")
            box_file_id = err.context_info["conflicts"]["id"]
            box_file = box_client.file(file_id=box_file_id).get()
            try:
                box_file.update_contents(path_to_file)
            except BoxAPIException as err2:
                logging.error("Failed to update %s: %s", box_file.name, err2)
                raise err2
        else:
            raise err

    return box_file
```
Then upload the `workshops/files/content_samples/sample_file.txt` file to the `files` folder.
```python
    sample_file = upload_file(
        client, files_root, "workshops/files/content_samples/sample_file.txt"
    )
    print(f"Uploaded {sample_file.name} to {files_root.name}")
```
Resuting in:
```
WARNING:root:File already exists, updating contents
Uploaded sample_file.txt to files
```
From a code perspective it isn't much different, so why should I use th preflight check?
The preflight check is a good way to validate if a file can be uploaded before actually uploading it.
Imagine running out of space quota after a long upload, it would be a waste of time and resources.

## Download file
Now let's try to download the file we just uploaded.
Create a method named `download_file` that receives a `file` and a `local_path` and downloads the file.

```python
def download_file(box_file: File, local_path_to_file: str):
    """Download a file from Box"""

    with open(local_path_to_file, "wb") as file_stream:
        box_file.download_to(file_stream)
```
Then download the `sample_file.txt` file to the root of your project.
```python
    download_file(sample_file, "./sample_file_downloaded.txt")

    for local_file in os.listdir("./"):
        if local_file.endswith(".txt"):
            print(local_file)
```
Resulting in:
```
WARNING:root:File already exists, updating contents
requirements.txt
sample_file_downloaded.txt
```

## Download a ZIP
When you need to download muiple files and folders at once, you can use the `download_zip` method of the `client` object.
Create a method named `download_zip` that receives a `client` and a list of `items` and downloads the folder as a zip file to a `local_path`.

```python
def download_zip(
    box_client: Client, local_path_to_zip: str, box_items: Iterable["Item"]
):
    """Download a zip file from Box"""
    file_name = os.path.basename(local_path_to_zip)
    with open(local_path_to_zip, "wb") as file_stream:
        box_client.download_zip(file_name, box_items, file_stream)
```
Then lets zip the entire `root` folder:
```python
    user_root = client.folder(folder_id="0").get()

    items = []
    for item in user_root.get_items():
        items.append(item)

    print("Downloading zip")
    download_zip(client, "./sample_zip_downloaded.zip", items)

    for local_file in os.listdir("./"):
        if local_file.endswith(".zip"):
            print(local_file)
```
Resulting in:
```
Downloading zip
sample_zip_downloaded.zip
```
If you open the zip file you should see all content stored by your user.
Note that the `items` list can be any combination of `files` and `folders`.


## Extra Credit
There are many more methods you can try for the file object.
Try them out and see what you can find:
* []()
* []()
* []()
* []()

# Final thoughts










