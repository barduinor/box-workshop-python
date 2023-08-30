# File Representations
A representation is an alternative asset for a file stored in Box. These assets can be PDFs, thumbnails, or text extractions.

Representations are automatically generated for the supported file types, either when uploading to Box or when requesting the asset.


## Concepts
Consider file representations as document avatars.
Representations go way beyond thumbnails, they are a way to access the content of a file without having to download it or get a pdf version of a document, even if the document is not a pdf.

This feature has become more relevant with the rise of AI and LLM, as it allows you to extract the content of a file and use it for other purposes, for example sending it to OpenAI.

Not all representations are availabe for all file types. For example, you can't get a text representation of an image file.

## File Representations API
References to our documentation:
* [SDK Files](https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md#get-file-representations)
* [API Guide](https://developer.box.com/guides/representations/)
* [API Reference ](https://developer.box.com/reference/get-files-id/)


# Exercises
## Setup
Create a `files_representations_init.py` file on the root of the project and execute the following code:
```python
"""create sample content to box"""
import logging
from utils.config import AppConfig

from utils.box_client import get_client

from workshops.file_representations.create_samples import create_samples

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


if __name__ == "__main__":
    client = get_client(conf)
    create_samples(client)
```
Result:
```
INFO:root:      Folder workshops (223095001439)
INFO:root:      Folder file_representations (223939315135)
INFO:root:      File uploaded Single Page.docx (1294096878155)
INFO:root:      File uploaded JS-Small.js (1294098434302)
INFO:root:      File uploaded HTML.html (1294094879490)
INFO:root:      File uploaded Document (PDF).pdf (1294102659923)
INFO:root:      File uploaded Audio.mp3 (1294103505129)
INFO:root:      File uploaded Preview SDK Sample Excel.xlsx (1294097951585)
INFO:root:      File uploaded JSON.json (1294102660561)
INFO:root:      File uploaded ZIP.zip (1294105019347)
INFO:root:      File uploaded Document (Powerpoint).pptx (1294096083753)
```

Next, create a `files_representations_init.py` file on the root of the project that you will use to write your code.
Create a global constant named `REPRESENTATIONS_LINKS_ROOT` and make it equal to the id of the `file_representations` folder, in my case `223939315135`.

Create a global constants for each file with their file id that you got on the previous step.
In my case:
```python
FILE_DOCX = 1294096878155
FILE_JS   = 1294098434302
FILE_HTML = 1294094879490
FILE_PDF  = 1294102659923
FILE_MP3  = 1294103505129
FILE_XLSX = 1294097951585
FILE_JSON = 1294102660561
FILE_ZIP  = 1294105019347
FILE_PPTX = 1294096083753
```

```python
"""Box File representations"""

import logging
from boxsdk import Client

from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.object.item import Item

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()

FILE_DOCX = 1294096878155
FILE_JS = 1294098434302
FILE_HTML = 1294094879490
FILE_PDF = 1294102659923
FILE_MP3 = 1294103505129
FILE_XLSX = 1294097951585
FILE_JSON = 1294102660561
FILE_ZIP = 1294105019347
FILE_PPTX = 1294096083753


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    client = get_client(conf)

    user = client.user().get()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")


if __name__ == "__main__":
    main()

```


## List all representations for a file
Let's start by creating a couple of methods that list and print all representation for a file object:
```python
def file_representations_print(file_name: str, representation: List[dict]):
    json_str = json.dumps(representation, indent=4)
    print(f"\nFile {file_name} has {len(representation)} representations:\n")
    print(json_str)

def file_representations(file: File, rep_hints: str = None) -> List[dict]:
    return file.get_representation_info(rep_hints)
```
Then use it in your main method with the `FILE_DOCX`:
```python
def main():
    """Simple script to demonstrate how to use the Box SDK"""
    client = get_client(conf)

    user = client.user().get()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    file_docx = client.file(FILE_DOCX).get()

    file_docx_representations = file_representations(file_docx)
    file_representations_print(file_docx.name, file_docx_representations)
```
Resulting in:
```
Hello, I'm Free Dev 001 (barduinor+001@gmail.com) [25428698627]

File Single Page.docx has 9 representations:
...
```
Quite a lot info there, let's check this one that represents a file thumbnail:
```json
    {
        "representation": "jpg",
        "properties": {
            "dimensions": "32x32",
            "paged": "false",
            "thumb": "true"
        },
        "info": {
            "url": "https://api.box.com/2.0/internal_files/1294096878155/versions/1415005971755/representations/jpg_thumb_32x32"
        }
    },
```

## Get a specific representation
In order to get a specific representation, you need to use the `representation hints` parameter on the method.
For example, to get the png 1024x1024 representation of the `FILE_DOCX`:
```python
def main():
    ...

    file_docx_representations_png = file_representations(file_docx, "[jpg?dimensions=320x320]")
    file_representations_print(file_docx.name, file_docx_representations_png)
```
Resulting in:
```json
[
    {
        "representation": "jpg",
        "properties": {
            "dimensions": "320x320",
            "paged": "false",
            "thumb": "false"
        },
        "info": {
            "url": "https://api.box.com/2.0/internal_files/1294096878155/versions/1415005971755/representations/jpg_320x320"
        },
        "status": {
            "state": "success"
        },
        "content": {
            "url_template": "https://public.boxcloud.com/api/2.0/internal_files/1294096878155/versions/1415005971755/representations/jpg_320x320/content/{+asset_path}"
        }
    }
]
```
Notice that the `state` is `success`, this means that the representation has been generated. If the representation is not available then the state will be `none`.

## Download the representation
Now that we have the `url_template` we can download the representation.
First let's create the simplest method to download a file from a url:
```python
def do_request(url: str, access_token: str):
    resp = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    resp.raise_for_status()
    return resp.content
```
Next let's create a representation download method:
```python
def representation_download(access_token: str, file_representation: str, file_name: str):
    if file_representation["status"]["state"] != "success":
        print(f"Representation {file_representation['representation']} is not ready")
        return

    url_template = file_representation["content"]["url_template"]
    url = url_template.replace("{+asset_path}", "")
    file_name = file_name.replace(".", "_") + "." + file_representation["representation"]

    content = do_request(url, access_token)

    with open(file_name, "wb") as file:
        file.write(content)

    print(f"Representation {file_representation['representation']} saved to {file_name}")
```
And finally use it in your main method:
```python
def main():
    ...

    representation_download(
        client.auth.access_token, 
        file_docx_representations_png[0], 
        file_docx.name
        )
```
My end result:
```json
[
    {
        "representation": "jpg",
        "properties": {
            "dimensions": "320x320",
            "paged": "false",
            "thumb": "false"
        },
        "info": {
            "url": "https://api.box.com/2.0/internal_files/1294096878155/versions/1415005971755/representations/jpg_320x320"
        },
        "status": {
            "state": "success"
        },
        "content": {
            "url_template": "https://public.boxcloud.com/api/2.0/internal_files/1294096878155/versions/1415005971755/representations/jpg_320x320/content/{+asset_path}"
        }
    }
]
```
And a new file has been downloaded to my local folder:

![Single Page_docx.jpg](./img/Single%20Page_docx.jpg)

## Get thumbnail representation
The python SDK as a helper method to get the thumbnail representation of a file:
Let's create a specific method for it:
```python
def file_thubmnail(file: File, dimensions: str, representation: str) -> bytes:
    thumbnail = file.get_thumbnail_representation(dimensions, representation)
    if not thumbnail:
        raise Exception(f"Thumbnail for {file.name} not available")
    return thumbnail
```
Notice that the requested thubmnail is not always available. If not we're generating an  exception, in which case you should select another representation.

Let's use it in our main method:
```python
def main():
    ...

    file_docx_thumbnail = file_thubmnail(file_docx, "94x94", "jpg")
    print(f"\nThumbnail for {file_docx.name} saved to {file_docx.name.replace('.', '_')}_thumbnail.jpg")
    with open(file_docx.name.replace(".", "_").replace(" ", "_") + "_thumbnail.jpg", "wb") as file:
        file.write(file_docx_thumbnail)
```
Resulting in:
```
Thumbnail for Single Page.docx saved to Single Page_docx_thumbnail.jpg
```
And I have a new file on my local folder:

![Single Page_docx_thumbnail.jpg](./img/Single_Page_docx_thumbnail.jpg)

## Get PDF representation
TODO: Add PDF representation

## Get text representation
`NOT WORKING`
Let's use our generic representation method to get the text representation of the `FILE_PDF':
```python

## Extra Credit
There are a few more things you can do:

# Final thoughts


