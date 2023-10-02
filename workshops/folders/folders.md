# Folders
Folders, together with Files, are at the core of the Box API. 
Folders can be uploaded and downloaded, as well as hold important metadata information about the content.
They are the primary way to organize content in Box.
## Concepts
Box is not a file systems, but it does have a concept of folders, even if it is a somewhat virtual concept.
This is because of the users familiarity with file systems, and the need to organize content.
So a folder is essentially a container of items (files and folders), with a nested parent folder.

Folder id 0 is the root folder for the user, and it is the only folder that does not have a parent folder.
Folder names must be unique within the parent folder.


## Folder API
References to our documentation:
* [SDK Folder](https://github.com/box/box-python-sdk/blob/main/docs/usage/folders.md)
* [API Folder Guide](https://developer.box.com/guides/folders/)
* [API Reference](https://developer.box.com/reference/resources/folder/)


# Exercises
## Setup
Create a `folders_init.py` file on the root of the project and execute the following code:
```python
"""create sample content to box"""
import logging
from utils.config import AppConfig

from utils.box_client import get_client

from workshops.folders.create_samples import create_samples

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


if __name__ == "__main__":
    client = get_client(conf)
    create_samples(client)
```
Result:
```
INFO:root:Folder workshops with id: 208856587587
INFO:root:Folder folders with id: 209376706619
```
`Each id is unique to your Box account, so your results will be different.`

Open your Box account and verify that the following content was uploaded:
```
- workshops
    - folders
```


Next, create a `folders.py` file on the root of the project that you will use to write your code:
```python
"""Box Folder workshop"""
import logging
from typing import Iterable

from boxsdk import Client, BoxAPIException
from boxsdk.object.item import Item
from boxsdk.object.folder import Folder

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def print_box_item(box_item: Item, level: int = 0):
    """Basic print of a Box Item attributes"""
    print(
        f"{'   ' * level}({box_item.id}) {box_item.name}{'/' if box_item.type == 'folder' else ''}"
    )


def print_box_items(box_items: Iterable["Item"]):
    """Print items"""
    print("--- Items ---")
    for box_item in box_items:
        print_box_item(box_item)
    print("-------------")

if __name__ == "__main__":
    client = get_client(conf)
```

## List folder content
Create a method to list the content of a folder, by id.
Make the default folder id the root folder id.
List the contents of the root folder.
```python
def get_folder_items(box_client: Client, box_folder_id: str = "0") -> Iterable["Item"]:
    """Get folder items"""
    folder = box_client.folder(folder_id=box_folder_id).get()
    return folder.get_items()


if __name__ == "__main__":
    client = get_client(conf)

    items = get_folder_items(client)
    print_box_items(items)
```
Should result in something similar to:
```
--- Items ---
Type: folder ID: 208856587587 Name: workshops
Type: file ID: 1204688948039 Name: Get Started with Box.pdf
-------------
```
## List folder content recursively
Create a method to list the content of a folder, by id, recursively.
```python
def print_folder_items_recursive(
    box_client: Client, folder: Folder, level: int = 0
) -> Iterable["Item"]:
    """Get folder items recursively"""
    print_box_item(folder, level)
    box_items = folder.get_items()
    for box_item in box_items:
        if box_item.type == "folder":
            print_folder_items_recursive(box_client, box_item, level + 1)
        else:
            print_box_item(box_item, level + 1)
```
Call the method with the root folder:
```python
root_folder = client.folder(folder_id="0").get()
print_folder_items_recursive(client, root_folder)
```
Should result in something similar to:
```
(0) All Files/
   (209408240392) workshops/
      (209410865444) folders/
   (1204688948039) Get Started with Box.pdf
```

## Create a method to always return the folder `folders`
```python
def get_workshop_folder(box_client: Client) -> Folder:
    """Get workshop folder"""
    root = box_client.folder(folder_id="0").get()
    workshops_folder_list = [
        box_item
        for box_item in root.get_items()
        if box_item.name == "workshops" and box_item.type == "folder"
    ]
    if workshops_folder_list == []:
        raise ValueError("'Workshops' folder not found")

    folders_folder_list = [
        box_item
        for box_item in workshops_folder_list[0].get_items()
        if box_item.name == "folders" and box_item.type == "folder"
    ]
    if folders_folder_list == []:
        raise ValueError("'Folders' folder not found")

    return folders_folder_list[0]
```
And then test it:
```python
wksp_folder = get_workshop_folder(client)
print_box_item(wksp_folder)
```
Result:
```
(209410865444) folders/
```
This example serves to illustrate how to navigate the folder structure, amd as you can see this is not very practical.

There is no path navigation in Box, so make sure your app keeps track of the folder ids it needs to access.

## Creating folders
Create a method to create subfolder in a parent folder, returning the created folder.
If the folder already exists just return the exiting folder. 
```python
def create_box_folder(
    box_client: Client, folder_name: str, parent_folder: Folder
) -> Folder:
    """create a folder in box"""

    try:
        folder = parent_folder.create_subfolder(folder_name)
    except BoxAPIException as box_err:
        if box_err.code == "item_name_in_use":
            box_folder_id = box_err.context_info["conflicts"][0]["id"]
            folder = box_client.folder(box_folder_id).get()
        else:
            raise box_err

    return folder
```
And test it with:
```python
wksp_folder = get_workshop_folder(client)
my_documents = create_box_folder(client, "my_documents", wksp_folder)
print_folder_items_recursive(client, wksp_folder)
```
Resulting in:
```
INFO:root:Folder my_documents with id: 209418602837
(209410865444) folders/
   (209418602837) my_documents/
```

## Creating a few more folders
Create a folder structure like this:
```
- workshops
    - folders
        - my_documents
            - work
        - downloads
            - personal
```
```python
wksp_folder = get_workshop_folder(client)

my_documents = create_box_folder(client, "my_documents", wksp_folder)
work = create_box_folder(client, "work", my_documents)

downloads = create_box_folder(client, "downloads", wksp_folder)
personal = create_box_folder(client, "personal", downloads)

print_folder_items_recursive(client, wksp_folder)
```    
Resulting in:
```
(209410865444) folders/
   (209415893720) downloads/
      (209418487331) personal/
   (209418602837) my_documents/
      (209416741156) work/
```
## Copy folders
Copy the `personal` folder to the `my_documents` folder.
If the folder already exists just return the exiting folder.
This is an example of how to handle error in Box.
```python
try:
    my_docs_personal = personal.copy(parent_folder=my_documents)
except BoxAPIException as err:
    if err.code == "item_name_in_use":
        folder_id = err.context_info["conflicts"]["id"]
        my_docs_personal = client.folder(folder_id).get()
    else:
        raise err
print_folder_items_recursive(client, wksp_folder)
```


Resulting in:
```
(209410865444) folders/
   (209415893720) downloads/
      (209418487331) personal/
   (209418602837) my_documents/
      (209419371366) personal/
      (209416741156) work/
```

## Update a folder
Add a description to the `downloads` folder.
```python
downloads.update_info(
    data={
        "description": "This is where my downloads go, remember to clean it once in a while"
    }
)
print(f"{downloads.type} {downloads.id} {downloads.name}")
print(f"Description: {downloads.description}")
```
Resulting in:
```
folder 209415893720 downloads
Description: This is where my downloads go, remember to clean it once in a while
```
## Delete a folder
Create a new folder called `tmp` inside `downloads`
Create a new folder called `tmp2` inside `tmp`
Delete folder `tmp` and all its contents.

The delete method accepts a `recursive` parameter that defaults to `True`, deleting all the contents of the folder, `no questions asked`.

So `be careful` when using it.

```python
    tmp = create_box_folder(client, "tmp", downloads)
    tmp2 = create_box_folder(client, "tmp2", tmp)

    print("--- Before the delete ---")
    print_folder_items_recursive(client, downloads)
    print("---")

    try:
        tmp.delete(recursive=False)
    except BoxAPIException as err:
        if err.code == "folder_not_empty":
            print(f"Folder {tmp.name} is not empty, deleting recursively")
            try:
                tmp.delete()
            except BoxAPIException as err_l2:
                raise err_l2
        else:
            raise err

    print("--- After the delete ---")
    print_folder_items_recursive(client, downloads)
    print("---")

```
Resulting in:
```
--- Before the delete ---
(209415893720) downloads/
   (209425834438) personal/
   (209428556202) tmp/
      (209428169977) tmp2/
---
Folder tmp is not empty, deleting recursively
--- After the delete ---
(209415893720) downloads/
   (209425834438) personal/
---
```
## Rename a folder
Rename the `personal` folder under `downloads` to `games`.

What were you thinking? This is a corporate laptop!!!

Delete the `games` folder
```python
print("Renaming personal download to games")
games = personal.rename("games")
print_folder_items_recursive(client, downloads)
print("---")

print("Deleting games")
games.delete()
print_folder_items_recursive(client, downloads)
print("---")
```
Resulting in:
```
Renaming personal download to games
(209415893720) downloads/
   (209433012423) games/
---
Deleting games
(209415893720) downloads/
---
```
## Extra Credit
There are many more methods you can try for the folder object.
Try them out and see what you can find:
* [Move](https://github.com/box/box-python-sdk/blob/main/docs/usage/folders.md#move-a-folder)
* [Create a Folder Lock](https://github.com/box/box-python-sdk/blob/main/docs/usage/folders.md#create-a-folder-lock)
* [Get Folder Locks](https://github.com/box/box-python-sdk/blob/main/docs/usage/folders.md#get-folder-locks)
* [Delete a Folder Lock](https://github.com/box/box-python-sdk/blob/main/docs/usage/folders.md#delete-a-folder-lock)

# Final thoughts

`Folders` are the primary way to organize content in Box.

They are a virtual concept, but they are very familiar to users.

Folder id 0 is the root folder for the user, and it is the only folder that does not have a parent folder.

Folder names must be unique within the parent folder.

There is no path navigation in Box, so make sure your app keeps track of the folder ids it needs to access.








