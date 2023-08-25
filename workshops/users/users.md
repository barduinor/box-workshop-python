# Users
The Box API supports a variety of users, ranging from real employees logging in with their Managed User account, to applications using App Users to drive powerful automation workflows.
## Concepts
There are several types of users in Box. Typically they are divided into two categories: Managed Users and service accounts. Managed Users are real people who have Box accounts. 

Service accounts are special users that are created by applications to represent a service account. Service accounts are not real people, but they can be used to represent a service account or an application user for an application. Service accounts are not visible in the Box web application, and can only be accessed via the API.

For more information on the different types of users, see the [User Types](https://developer.box.com/guides/getting-started/user-types/) on our getting started guide.

## Users API
References to our documentation:
* [Users Guide](https://developer.box.com/guides/users/)
* [Users API Reference](https://developer.box.com/reference/resources/user/)
* [Python SDK - Users](https://github.com/box/box-python-sdk/blob/main/docs/usage/user.md)


# Exercises
## Setup
Hopefully you have a google email account handy, or some way to create email aliases, or multiple email accounts.

This in GMail is very simple, if your email is myname@gmail.com then you can simply use mayname+001@gmail.com as an alias.
This will allow you to create multiple users in Box, but only have to manage one email account.

## Who am I?
The User object is the main object that represents a user in Box. It contains all the information about a user, including their name, email, and other information.

Create a `users.py` file on the root of the project and execute the following code:
```python
"""Box Users workshop"""
import logging
import os
from typing import Iterable

from boxsdk import Client, BoxAPIException
from boxsdk.object.item import Item
from boxsdk.object.folder import Folder
from boxsdk.object.file import File
from boxsdk.object.user import User

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()

def main():
    """
    Simple script to demonstrate how to use the Box SDK
    with oAuth2 authentication
    """
    client = get_client(conf)

    user = client.user().get()
    print(f"Hello, {user.name}, ({user.login})")


if __name__ == "__main__":
    main()
```
This, in my case results in the following output:
```bash
Hello, Free Dev 001, (barduinor+001@gmail.com)
```
Having a call to `client.user().get()` without specifying the user id is a good way to identify who is logged in. To be precise it identifies the underlying user account context of the client.
More on this later.

## The user object
The user object is a very rich object, with a lot of information about the user.
Create a method to retreive the user object:
```python
def get_user_by_id(client: Client, user_id: str) -> User:
    return client.user(user_id).get()
```
and use it in your main method with a user id of `me`:
```python
def main():
    ...

    me = get_user_by_id(client, "me")
    print(f"\nHello there, {user.name}, ({user.login}) [{user.id}]")
```
Resulting in:
```bash
Hello there, Free Dev 001, (barduinor+001@gmail.com) [25428698627]
```
The `user_id="me"` is a special value that will return the user object of the underlying user account context of the client.


## Create a managed user
The Box API supports creating new users in an enterprise.
Create a method to create a new user:
```python
def create_user(client: Client, name: str, login: str) -> User:
    return client.create_user(name, login)
```

and use it in your main method:
```python
## 


## 

## Extra Credit

# Final thoughts










