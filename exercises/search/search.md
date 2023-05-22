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
```
File and Folder are extensive objects.
For the sake of simplicity, we will use the Item object, which is the base class for both File and Folder.
It contains the fields common to both, such as id, name, description, etc.
```

## Simple search
Create a method to search for any content type by a given query string.
Test using "Box" as a query.

## Try combining queries using AND, OR, and NOT
* "Box AND API" should return items with both "Box" and "API" in the name
* "Box OR API" should return items with either "Box" or "API" in the name
* "Box NOT API" should return items with "Box" in the name, but not "API"

## Try searching for specific content types
Limit the search to name:
* "name:Box" should return items with "Box" in the name

## Try searching for specific types
Limit the search to folders:
* "type:folder" should return only folders

## Try searching only in specific folders
Limit the search to a specific folder:

## Try limiting the output
Limit the output to id, name, and description.








