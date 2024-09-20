from .client import BaseClient
from googleapiclient.http import MediaIoBaseDownload


class DriveClient(BaseClient):

    def __init__(
            self,
            client_secret_path="credentials/secret.json",
            credentials_path="credentials/credentials.json",
            data_folder="test",
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
        self.data_folder = data_folder

    def get_files(self, folder_id):
        page_token = None
        while True:
            # Call the Drive v3 API
            results = self.service.files().list(
                q=f"'{folder_id}' in parents",
                pageSize=10, fields="nextPageToken, files(id, name)",
                pageToken=page_token).execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                for item in items:
                    print(f'{item["name"]} ({item["id"]})')

                    file_id = item['id']
                    request = self.service.files().export(fileId=file_id, mimeType='text/csv')

                    with open(f"{self.data_folder}/{item['name']}.csv", 'wb') as fh:
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while done is False:
                            status, done = downloader.next_chunk()
                            print(
                                f"Download {int(status.progress() * 100)}%.", end="\r")
                            print()

            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
