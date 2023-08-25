"""Box File Comments"""

import logging

from boxsdk import Client, BoxAPIException
from boxsdk.object.file import File
from boxsdk.object.comment import Comment

from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()

COMMENTS_ROOT = "223269791429"
SAMPLE_FILE = "1290064263703"


def file_comments_print(client: Client, file: File):
    """Print all comments for a file"""
    comments = file.get_comments()
    print(f"\nComments for file {file.name} ({file.id}):")
    print("-" * 10)
    for comment in comments:
        print(f"{comment.message} by {comment.created_by.name} ({comment.created_at})")
    print("-" * 10)


def file_comment_add(client: Client, file: File, message: str) -> Comment:
    """Add a comment to a file"""
    return file.add_comment(message)


def file_comment_reply(client: Client, comment: Comment, message: str) -> Comment:
    """Reply to a comment"""
    return comment.reply(message)


def file_comment_delete(client: Client, comment: Comment):
    """Delete a comment"""
    try:
        comment.delete()
    except BoxAPIException as err:
        if err.status != 404:
            raise err


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    client = get_client(conf)

    user = client.user().get()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    file = client.file(SAMPLE_FILE).get()

    # print file comments
    file_comments_print(client, file)

    # add another comment
    comment = file_comment_add(client, file, "What is this file about?")
    file_comments_print(client, file)

    # reply to the last comment
    comment_reply = file_comment_reply(client, comment, "I hear you!!! This is a sample file")
    file_comments_print(client, file)

    # delete all comments
    file_comment_delete(client, comment_reply)
    comments = file.get_comments()
    for comment in comments:
        file_comment_delete(client, comment)
    file_comments_print(client, file)


if __name__ == "__main__":
    main()
