"""Box File representations"""

import json
import logging
import requests
from typing import List

from boxsdk.object.file import File
from boxsdk.object.folder import Folder


from utils.config import AppConfig
from utils.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()
DEMO_FOLDER = 223939315135
FILE_DOCX = 1294096878155
FILE_JS = 1294098434302
FILE_HTML = 1294094879490
FILE_PDF = 1294102659923
FILE_MP3 = 1294103505129
FILE_XLSX = 1294097951585
FILE_JSON = 1294102660561
FILE_ZIP = 1294105019347
FILE_PPTX = 1294096083753


def file_representations_print(file_name: str, representation: List[dict]):
    json_str = json.dumps(representation, indent=4)
    print(f"\nFile {file_name} has {len(representation)} representations:\n")
    print(json_str)


def file_representations(file: File, rep_hints: str = None) -> List[dict]:
    return file.get_representation_info(rep_hints)


def do_request(url: str, access_token: str):
    resp = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    resp.raise_for_status()
    return resp.content


def representation_download(access_token: str, file_representation: str, file_name: str):
    if file_representation["status"]["state"] != "success":
        print(f"Representation {file_representation['representation']} is not ready")
        return

    url_template = file_representation["content"]["url_template"]
    url = url_template.replace("{+asset_path}", "")
    file_name = file_name.replace(".", "_").replace(" ", "_") + "." + file_representation["representation"]

    content = do_request(url, access_token)

    with open(file_name, "wb") as file:
        file.write(content)

    print(f"Representation {file_representation['representation']} saved to {file_name}")


def file_thubmnail(file: File, dimensions: str, representation: str) -> bytes:
    thumbnail = file.get_thumbnail_representation(dimensions, representation)
    if not thumbnail:
        raise Exception(f"Thumbnail for {file.name} not available")
    return thumbnail


def folder_list_representation_status(folder: Folder, representation: str):
    items = folder.get_items()
    print(f"\nChecking for {representation} status in folder [{folder.name}] ({folder.id})")
    for item in items:
        if isinstance(item, File):
            file_repr = file_representations(item, "[" + representation + "]")
            if file_repr:
                state = file_repr[0].get("status").get("state")
            else:
                state = "not available"
            print(f"File {item.name} ({item.id}) state: {state}")


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    client = get_client(conf)

    user = client.user().get()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    file_docx = client.file(FILE_DOCX).get()

    file_docx_representations = file_representations(file_docx)
    file_representations_print(file_docx.name, file_docx_representations)

    file_docx_representations_png = file_representations(file_docx, "[jpg?dimensions=320x320]")
    file_representations_print(file_docx.name, file_docx_representations_png)

    representation_download(client.auth.access_token, file_docx_representations_png[0], file_docx.name)

    file_docx_thumbnail = file_thubmnail(file_docx, "94x94", "jpg")
    print(f"\nThumbnail for {file_docx.name} saved to {file_docx.name.replace('.', '_')}_thumbnail.jpg")
    with open(file_docx.name.replace(".", "_").replace(" ", "_") + "_thumbnail.jpg", "wb") as file:
        file.write(file_docx_thumbnail)

    file_ppt = client.file(FILE_PPTX).get()
    print(f"\nFile {file_ppt.name} ({file_ppt.id})")
    file_ppt_repr_pdf = file_representations(file_ppt, "[pdf]")
    file_representations_print(file_ppt.name, file_ppt_repr_pdf)
    representation_download(client.auth.access_token, file_ppt_repr_pdf[0], file_ppt.name)

    folder = client.folder(DEMO_FOLDER).get()
    folder_list_representation_status(folder, "extracted_text")

    file_ppt_repr = file_representations(file_ppt, "[extracted_text]")
    file_representations_print(file_ppt.name, file_ppt_repr)

    if file_ppt_repr[0].get("status").get("state") == "none":
        info_url = file_ppt_repr[0].get("info").get("url")
        do_request(info_url, client.auth.access_token)

    file_ppt_repr = file_representations(file_ppt, "[extracted_text]")
    file_representations_print(file_ppt.name, file_ppt_repr)

    representation_download(client.auth.access_token, file_ppt_repr[0], file_ppt.name)


if __name__ == "__main__":
    main()
