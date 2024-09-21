from .client import BaseClient
from googleapiclient.errors import HttpError

import time


class SheetsClient(BaseClient):

    def __init__(
            self,
            client_secret_path="data/secret.json",
            credentials_path="data/credentials.json",
            force_renew=False
    ) -> None:
        super().__init__(
            "sheets",
            "v4",
            client_secret_path,
            credentials_path,
            [
                "https://www.googleapis.com/auth/spreadsheets.readonly"
            ],
            force_renew
        )

    def get_spreadsheet(self, spreadsheetId, range_="Attendees"):
        spreadsheet = {}
        for _ in range(5):
            try:
                time.sleep(1)

                spreadsheet["data"] = list(
                    (self
                        .service
                        .spreadsheets()
                        .values()
                        .get(spreadsheetId=spreadsheetId, range=range_)
                        .execute()
                     )
                    .get("values"))

                data = (self
                        .service
                        .spreadsheets()
                        .get(spreadsheetId=spreadsheetId)
                        .execute()
                        )
                spreadsheet["title"] = data.get("properties").get("title")
                return spreadsheet

            except (TimeoutError, HttpError) as e:
                print("Google spreadsheets' read operation timed out, trying again.")

        return None
