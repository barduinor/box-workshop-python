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

```

Open your Box account and verify that the following content was uploaded:
```

```


Next, create a `files.py` file on the root of the project that you will use to write your code:
```python
"""Box Files workshop"""
import logging
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


if __name__ == "__main__":
    client = get_client(conf)

```

## Simple file upload

```python

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










