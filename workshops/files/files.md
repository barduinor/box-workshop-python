# Files


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

```

Open your Box account and verify that the following content was uploaded:
```

```


Next, create a `files.py` file on the root of the project that you will use to write your code:
```python

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

```

## Extra Credit
There are many more methods you can try for the file object.
Try them out and see what you can find:
* []()
* []()
* []()
* []()

# Final thoughts










