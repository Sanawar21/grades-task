from .client import BaseClient

import os
from googleapiclient.http import MediaIoBaseDownload


class DriveClient(BaseClient):

    def __init__(
            self,
            client_secret_path="credentials/secret.json",
            credentials_path="credentials/credentials.json",
            force_renew=False
    ) -> None:
        super().__init__(
            "drive",
            "v3",
            client_secret_path,
            credentials_path,
            [
                "https://www.googleapis.com/auth/drive.readonly"
            ],
            force_renew
        )

    def download_files(self, folder_id, output_path: str = ".temp"):
        page_token = None
        file_index = 0

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        while True:
            results = self.service.files().list(
                q=f"'{folder_id}' in parents",
                pageSize=10, fields="nextPageToken, files(id, name)",
                pageToken=page_token
            ).execute()

            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                for item in items:
                    file_id = item["id"]
                    request = self.service.files().get_media(fileId=file_id)
                    with open(f"{output_path}/{file_index}.xlsx", 'wb') as f:
                        file_index += 1
                        downloader = MediaIoBaseDownload(f, request)
                        done = False
                        while not done:
                            _, done = downloader.next_chunk()
                            print(f"Downloading file {item['name']}")

            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
