# Searching Box
The Box API provides a way to find content in Box using full-text search queries. Support for the Box search API is available in all our supported SDKs and the CLI.
## Concepts
Box is not a file system.
Often developers expect the search to behave similar to a typical file system search, using paths, wildcards, and file or folder names.

Search in Box is an indexed database search.
It indexes name, description, tags, comments, and content up to the first 10k bytes.
Every time any of these get created, updated or deleted, the index is updated, asynchronously.

This means that the search index is not always up to date, taking a few minutes to update.
## Search API
The Search API can be accessed via the Client object.
For example, to search for the term "test" anywhere in your content, and printing the results:
```python
search_results = client.search().query(query="test")
for item in search_results:
    print(f"type: {item.type}, id: {item.id}, name: {item.name}")
```
The search API supports a number of parameters to refine your search via the query method:
```python
def query(
            self,
            query: str,
            limit: int = None,
            offset: int = 0,
            ancestor_folders: Iterable['Folder'] = None,
            file_extensions: Iterable[str] = None,
            metadata_filters: MetadataSearchFilters = None,
            result_type: str = None,
            content_types: Iterable[str] = None,
            scope: Optional[str] = None,
            created_at_range: Tuple[Optional[str], Optional[str]] = None,
            updated_at_range: Tuple[Optional[str], Optional[str]] = None,
            size_range: Tuple[Optional[int], Optional[int]] = None,
            owner_users: Iterable['User'] = None,
            trash_content: Optional[str] = None,
            fields: Iterable[str] = None,
            sort: Optional[str] = None,
            direction: Optional[str] = None,
            ...
    ) -> Iterable['Item']:
```
Refer to our [Search Guide](https://developer.box.com/reference/get-search/) and [API Documentation](https://developer.box.com/reference/get-search/) for more details.

# Exercises
## Setup
Create a `search_init.py` file on the root of the project and execute the following code:
```python
"""upload sample content to box"""
import logging
from utils.config import AppConfig

from utils.box_client import get_client

from exercises.search.upload_samples import upload_content_sample

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


if __name__ == "__main__":
    client = get_client(conf)
    upload_content_sample(client)
```
Open your Box account and verify that the following content was uploaded:
```
- workshops
    - search
        - apple
            - apple1.txt
            - apple2.txt
            - apple3.txt
        - apple banana
            - apple.txt
            - banana.txt
        - apple pineapple banana
            - apple.txt
            - banana.txt
            - pineapple.txt
        - banana
            - banana.txt
        - banana apple
            - apple.txt
            - banana.txt
        - pineapple
            - pineapple.txt
        
```

Next, create a `search.py` file on the root of the project that you will use to write your code.
```python
""" Searching Box exercises"""
import logging
from typing import Iterable

from boxsdk.object.item import Item

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def print_box_item(box_item: Item):
    """Basic print of a Box Item attributes"""
    print(f"Type: {box_item.type} ID: {box_item.id} Name: {box_item.name}, ")


def print_search_results(items: Iterable["Item"]):
    """Print search results"""
    print("--- Search Results ---")
    for item in items:
        print_box_item(item)
    print("--- End Search Results ---")


if __name__ == "__main__":
    client = get_client(conf)
```

File and Folder are extensive objects.
For the sake of simplicity, we will use the Item object, which is the base class for both File and Folder.
It contains the fields common to both, such as id, name, description, etc. You can modify the `print_box_item` function to print any of the fields available in the Item object.

## Simple search
Create a method to search for any content type by a given query string.
Test using "apple" as a query.
```python
def simple_search(query: str) -> Iterable["Item"]:
    """Search by query in any Box content"""

    return client.search().query(query=query)

if __name__ == "__main__":
    client = get_client(conf)

    # Simple Search
    search_results = simple_search("apple")
    print_search_results(search_results)
```
The output should be similar to:
```
❯ python search_sln.py 
--- Search Results ---
Type: folder ID: 208850093677 Name: apple banana, 
Type: folder ID: 208858841669 Name: apple, 
Type: folder ID: 208856751058 Name: apple pineapple banana, 
Type: folder ID: 208848037313 Name: banana apple, 
Type: file ID: 1220477661707 Name: apple.txt, 
Type: file ID: 1220476606374 Name: apple.txt, 
Type: file ID: 1220478477851 Name: apple.txt, 
Type: file ID: 1220478610566 Name: apple1.txt, 
Type: file ID: 1220479548719 Name: apple2.txt, 
Type: file ID: 1220481540143 Name: apple3.txt, 
--- End Search Results ---
```
Did you get any results?
If not, why?
The search API is an indexed search.
It takes a few minutes to index the content.
If you just uploaded the content, it may not be indexed yet.
Wait a few minutes and try again.

Noticed it pciked up:
* both files and folders
* items with "apple" in the name
* including "apple1", "apple2", and "apple3"
* did not include pineapple

## Add another search for apple banana
```python
# Expanded Search
search_results = simple_search("apple banana")
print_search_results(search_results)
```
Notcie we have expanded our search. Now it is returning anything with "apple" or "banana" or both in the name.

## Add another search for "apple banana" with the double quotes
```python
# "Exact" Search
search_results = simple_search('"apple banana"')
print_search_results(search_results)
```
Notice we have now limited the search to only items with "apple banana" in the name.
```
--- Search Results ---
Type: folder ID: 208850093677 Name: apple banana, 
--- End Search Results ---
```

## Try combining queries using AND, OR, and NOT
* `apple NOT banana` should return items with both "apple" but nor "banana"
* `apple AND pineapple` should return items with both "apple" and "pineapple"
* `pineapple OR banana` should return items with "pineaplpe" or "banana"

## More searches
Did you know that the plural of banana without the "b" is actually pineapple in 6 different languges?
Let's search for `ananas`:
```python
# More Searches
search_results = simple_search('ananas')
print_search_results(search_results)
```
```
--- Search Results ---
Type: file ID: 1220479104299 Name: pineapple.txt
Type: file ID: 1220468415414 Name: pineapple.txt
--- End Search Results ---
```
Where did the `ananas` come from?
Remember that the search doesn't look only at the name, but also at the description, tags, comments, and content.
`pineapple.txt` has the word `ananas` in the description and content.

## Try searching only in the name
Modify your search method to only search in the name.
```python
def simple_search(query: str, content_types: Iterable[str] = None) -> Iterable["Item"]:
    """Search by query in any Box content"""

    return client.search().query(query=query, content_types=content_types)
```
Now try searching for `ananas` again:
```python
# Search only in name
search_results = simple_search(
    "ananas",
    content_types=[
        "name",
    ],
)
print_search_results(search_results)
```
>Note: In Python a string is an Iterable of characters. Make sure you pass the content_types as a list.

You get an empty result:
```
--- Search Results ---
--- End Search Results ---
```

Now try searching for `ananas` in the name and description:
```python
# Search in name and description
search_results = simple_search(
    "ananas",
    content_types=[
        "name",
        "description",
    ],
)
print_search_results(search_results)
```
You should get:
```
--- Search Results ---
Type: file ID: 1220468415414 Name: pineapple.txt
Type: file ID: 1220479104299 Name: pineapple.txt
--- End Search Results ---
```

## Try searching for specific result types
You can limit the search to specific result types, like files or folders.
Modify your search method to accept a result_type parameter:
```python
def simple_search(
    query: str, content_types: Iterable[str] = None, result_type: str = None
) -> Iterable["Item"]:
    """Search by query in any Box content"""

    return client.search().query(
        query=query, content_types=content_types, result_type=result_type
    )
```
Limit the search to folders:
```python
# Search for folders only
search_results = simple_search("apple", result_type="folder")
print_search_results(search_results)
```
Returns only folders:
```
--- Search Results ---
Type: folder ID: 208850093677 Name: apple banana
Type: folder ID: 208858841669 Name: apple
Type: folder ID: 208848037313 Name: banana apple
Type: folder ID: 208856751058 Name: apple pineapple banana
--- End Search Results ---
```

## Try searching only in specific folders
You can limit the search to specific folders.
Modify your search method to accept a ancestor_folders parameter:
```python
def simple_search(
    query: str,
    content_types: Iterable[str] = None,
    result_type: str = None,
    ancestor_folders: Iterable["Folder"] = None,
) -> Iterable["Item"]:
    """Search by query in any Box content"""

    return client.search().query(
        query=query,
        content_types=content_types,
        result_type=result_type,
        ancestor_folders=ancestor_folders,
    )
```
In the sample content we have a `banana.txt` file in the all folders containing `banana` in the name.
Let's search for `banana` files but print the parent folder name:
```python
# Search banana
search_results = simple_search("banana")

print("--- Search Results ---")
for item in search_results:
    print(
        f"Type: {item.type} ID: {item.id} Name: {item.name} Folder: {item.parent.name}"
    )
print("--- End Search Results ---")
```
Returns:
```
--- Search Results ---
Type: folder ID: 208858913186 Name: banana Folder: search
Type: folder ID: 208850093677 Name: apple banana Folder: search
Type: folder ID: 208848037313 Name: banana apple Folder: search
Type: folder ID: 208856751058 Name: apple pineapple banana Folder: search
Type: file ID: 1220482412264 Name: banana.txt Folder: apple banana
Type: file ID: 1220481286015 Name: banana.txt Folder: banana
Type: file ID: 1220474895277 Name: banana.txt Folder: apple pineapple banana
Type: file ID: 1220480931465 Name: banana.txt Folder: banana apple
--- End Search Results ---
```
Modify your search to only search `banana` in the `banana apple` and `apple banana` folders, returning only files:
>The folder ids are specific to your Box account. Make sure you use the correct ids.
```python
# Ancestor Search
folder_apple_banana = client.folder("208850093677")
folder_banana_apple = client.folder("208848037313")
search_results = simple_search(
    "banana",
    ancestor_folders=[folder_apple_banana, folder_banana_apple],
    result_type="file",
)
for item in search_results:
    print(
        f"Type: {item.type} ID: {item.id} Name: {item.name} Folder: {item.parent.name}"
    )
```
Returns:
```
--- Search Results ---
Type: file ID: 1220482412264 Name: banana.txt Folder: apple banana
Type: file ID: 1220480931465 Name: banana.txt Folder: banana apple
--- End Search Results ---
```

## Extra Credit
There are many more parameters you can use to refine your search.
Try them out and see what you can find:
* file_extensions
* created_at_range
* updated_at_range
* size_range
* trash_content
* sort
* direction

# Final thoughts
Altoguh powerful, the search API was primarely designed to help users find content in Box, and may not be suited for all use cases:
* Box is not a file system, so it doesn't have paths.
* It is an indexed search, so it may take a few minutes for the content to be indexed.
* It indexes names, description, tags, comments often giving unexpected results to developers.










