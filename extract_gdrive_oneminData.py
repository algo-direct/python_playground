#!/usr/bin/env python
# coding: utf-8

# In[11]:


import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import io


# In[12]:


from googleapiclient.discovery import build


# In[13]:


from googleapiclient.errors import HttpError


# In[14]:


from googleapiclient.http import MediaIoBaseDownload


# In[15]:


SCOPES = ["https://www.googleapis.com/auth/drive"]


# In[16]:


creds = None


# In[17]:


if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)


# In[18]:


if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        print("Refreshing token")
        creds.refresh(Request())
    else:
        print("generating token")
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

    print("Saving token")
    with open("token.json", "w") as token:
        token.write(creds.to_json())
        token.close()


# In[19]:


def download_file(parent_path, file_data, service):
    try:
        this_path = os.path.join(parent_path, file_data["name"])
        if os.path.exists(this_path):
            return
        request = service.files().get_media(fileId=file_data["id"])
        fh = io.FileIO(this_path, mode="wb")
        downloader = MediaIoBaseDownload(fh, request, chunksize=32 * 1024 * 1024)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print("Download %d%%." % int(status.progress() * 100))
        print("Download Complete!")
    except HttpError as error:
        print(f"An error occurred: {error}")


def download_folder(parent_path, folder_data, depth, service):
    if depth > 5:
        print(f"Depth is greater than 5 ({depth}), returning")
        return
    this_path = os.path.join(parent_path, folder_data["name"])
    os.makedirs(this_path, exist_ok=True)
    # print(f"download_folder this_path:{this_path}")
    folder_id = folder_data["id"]
    response = (
        service.files().list(q=f"'{folder_id}' in parents", spaces="drive").execute()
    )
    # print(f"response in download folder:{response}")
    for r in response["files"]:
        print(f"this_path:{this_path} : {r['name']}: {r['mimeType']}, {r['id']}")
        if r["mimeType"] == "application/vnd.google-apps.folder":
            download_folder(this_path, r, depth + 1, service)
        if r["mimeType"] == "application/zip":
            download_file(this_path, r, service)


try:
    service = build("drive", "v3", credentials=creds)
    response = (
        service.files()
        .list(
            q="name='oneminutedata' and mimeType='application/vnd.google-apps.folder'",
            spaces="drive",
        )
        .execute()
    )
    print(f"response:{response}")
    folder_id = response["files"][0]["id"]
    response = (
        service.files().list(q=f"'{folder_id}' in parents", spaces="drive").execute()
    )
    for r in response["files"]:
        print(f"top: {r['name']}: {r['mimeType']}")
        if r["name"] in map(str, range(2017, 2097)):
            download_folder("data", r, 0, service)
    print("-------------------- DONE -----------------------")
except HttpError as ex:
    print(f"ex:{ex}")


# In[ ]:
