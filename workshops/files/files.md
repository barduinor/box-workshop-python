# Files
File objects represent individual files in Box. They can be used to download a file's contents, upload new versions, and perform other common file operations (move, copy, delete, etc.).


## Concepts
File objects represent individual files in Box. They can be used to download a file's contents, upload new versions, and perform other common file operations such as move, copy, and delete.

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
    ...

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
if __name__ == "__main__":
    ...

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

## Preflight check
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
if __name__ == "__main__":
    ...

    sample_file = upload_file(
        client, files_root, "workshops/files/content_samples/sample_file.txt"
    )
    print(f"Uploaded {sample_file.name} to {files_root.name}")
```
Resulting in:
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
When you need to download multiple files and folders at once, you can use the `download_zip` method of the `client` object.
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
if __name__ == "__main__":
    ...

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

## File information
Now that we have some files to play with, let's explore the file object.
The first thing is to get the file object, we can do that by using the `file` method of the `client` object.

Create a method that returns a file object based on the file id:
```python
def get_file_by_id(file_id: str) -> File:
    """Get a file by ID"""
    return client.file(file_id=file_id).get()
```
Next, let's create another method that serializes the file object into a dictionary:
```python
def file_to_json(file: File) -> dict:
    return {
        "id": file.id,
        "name": file.name,
        "size": file.size,
        "created_at": file.created_at,
        "modified_at": file.modified_at,
        "etag": file.etag,
        "sha1": file.sha1,
        "description": file.description,
        "path_collection": file.path_collection,
    }
```
Test this method on your main method:
```python
if __name__ == "__main__":
    ...

    file = get_file_by_id("1204688948039")
    file_json = file_to_json(file)
    print(file_json)
```
and you should get something like:
```json
{
   "id":"1289038683607",
   "name":"sample_file.txt",
   "size":42,
   "created_at":"2023-08-24T11:00:04-07:00",
   "modified_at":"2023-08-24T11:03:21-07:00",
   "etag":"1",
   "sha1":"715a6fe7d575e27934e16e474c290048829ffc54",
   "description":""
}
```
There are many more properties you can explore, check the [API Reference](https://developer.box.com/reference/resources/file/) for more information.

## Update a file
Now that we have a file object, let's try to update it.
Update the SAMPLE_FILE python constant with the id of the sample file inside your Box `All Files/workshops/files/` folder.
In my case:
```python
SAMPLE_FILE = "223097997181"
```

Create a method that updates the description of a file:
```python
def file_update_description(file: File, description: str) -> File:
    return file.update_info(data={"description": description})
```
Change the description of the previous file:
```python
if __name__ == "__main__":
    ...

    file = get_file_by_id(SAMPLE_FILE)
    file_json = file_to_json(file)
    print(file_json)

    file = file_update_description(file, "This is a sample file")
    file = get_file_by_id(SAMPLE_FILE)
    file_json = file_to_json(file)
    print("\n\nAfter update:")
    print(file_json)
```
Resulting in:
```json
{
   "id":"1289038683607",
   "name":"sample_file.txt",
   "size":42,
   "created_at":"2023-08-24T11:00:04-07:00",
   "modified_at":"2023-08-24T11:42:39-07:00",
   "etag":"2",
   "sha1":"715a6fe7d575e27934e16e474c290048829ffc54",
   "description":"This is a sample file"
}
```
## List the contents of a folder
We need a method to list the contents of a folder.
Add this method to your `files.py` file:
```python
def folder_list_contents(folder: Folder):
    items = folder.get_items()
    print(f"\nFolder [{folder.name}] content:")
    for item in items:
        print(f"   {item.type} {item.id} {item.name}")
```

## Copy a file
Now lets duplicate the file we just updated, and list the folder contents:
We can do this directly in our main method:
```python
if __name__ == "__main__":
    ...

    files_folder = client.folder(folder_id=FILES_ROOT).get()
    try:
        file_copied = file.copy(parent_folder=files_folder, name="sample_file_copy.txt")
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            logging.warning("File already exists, we'll use it")
            file_copied_id = err.context_info["conflicts"]["id"]
            file_copied = get_file_by_id(file_copied_id)
        else:
            raise err
    folder_list_contents(files_folder)
```
The try block is there to prevent the script from failing if the file already exists, since we'll be running this script multiple times.

Resulting in:
```
Folder [files] content:
   file 1289038683607 sample_file.txt
   file 1289100188824 sample_file_copy.txt
```

## Move a file
Now lets move the file we just copied to the root of the box account:
```python
if __name__ == "__main__":
    ...

    root_folder = client.folder(folder_id="0").get()
    try:
        file_moved = file_copied.move(parent_folder=root_folder)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            logging.warning("File already exists, we'll use it")
            file_moved_id = err.context_info["conflicts"]["id"]
            file_moved = get_file_by_id(file_moved_id)
        else:
            raise err
    folder_list_contents(root_folder)
```
Again we need a `try` block.

Resulting in:
```
Folder [All Files] content:
   folder 216797257531 My Signed Documents
   folder 221723756896 UIE Samples
   folder 223095001439 workshops
   file 1204688948039 Get Started with Box.pdf
   file 1289100188824 sample_file_copy.txt
```

## Delete a file
Finally we'll delete the file we just copied:
```python
if __name__ == "__main__":
    ...
    file_moved.delete()
    folder_list_contents(root_folder)
```
Resulting in:
```
Folder [All Files] content:
   folder 216797257531 My Signed Documents
   folder 221723756896 UIE Samples
   folder 223095001439 workshops
   file 1204688948039 Get Started with Box.pdf
```

## Extra Credit
There are many more methods you can try for the file object.
Try them out and see what you can find:
* Create a method to rename a file.
* Create a method that returns the complete path (operating system style) of a file object
* Implement the chunked upload method
* Implement the manual upload method 


# Final thoughts
`File` objects are very powerful, they allow you to perform many operations on files. This workshop only scratched the surface of what you can do with them.
We'll explore more of them in the other workshops.









