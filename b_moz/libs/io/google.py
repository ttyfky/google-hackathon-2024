import datetime
import os
import os.path
import pickle
from typing import Optional

import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from b_moz.libs.project import secret_path, local_username


class GoogleAuth:
    def __init__(self):
        self._scopes = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @classmethod
    def load_local_cred_file(cls, cred_filename) -> Optional[Credentials]:
        """Loads the credentials from the local file."""
        if os.path.exists(cred_filename):
            with open(cred_filename, "rb") as token:
                return pickle.load(token)
        return None

    @classmethod
    def _refresh_if_expired(cls, creds) -> Optional[Credentials]:
        if (
            creds
            and creds.expiry + datetime.timedelta(days=1) < datetime.datetime.now()
        ):
            # NOTE: creds.refresh(Request()) does not work for IAP credentials.
            # So, we just return None to force re-authentication.
            return None
        return creds


class GoogleDriveAuth(GoogleAuth):

    def __init__(self):
        super().__init__()

        self._CLIENT_SECRETS_FILE = os.path.normpath(
            os.path.join(secret_path(), "google_drive_client_secret.json")
        )

    @classmethod
    def local_drive_cred_filename(cls) -> str:
        return os.path.join(secret_path(), f"{local_username()}_drive.credentials")

    @classmethod
    def get_credentials(cls, client_id: str, client_secret: str):
        """Gets the credentials for the Google Drive."""
        with cls() as obj:
            cred_filename = obj.local_drive_cred_filename()
            creds = obj.load_local_cred_file(cred_filename)
            if creds and creds.expired and creds.refresh_token:
                # Try to renew the deadline
                creds.refresh(Request())
            # create cred file if not exists
            if creds is None or not creds.valid:
                port = 30001

                flow = InstalledAppFlow.from_client_config(
                    client_config={
                        "installed": {
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "response_type": "code",
                            "redirect_uris": [f"http://localhost:{port}"],
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://accounts.google.com/o/oauth2/token",
                        }
                    },
                    scopes=[
                        "openid",
                        "https://www.googleapis.com/auth/spreadsheets",
                        "https://www.googleapis.com/auth/userinfo.email",
                    ],
                )
                creds = flow.run_local_server(port=30001)  # type: ignore

                with open(cred_filename, "wb") as fo:
                    pickle.dump(creds, fo)
            return creds


class GoogleSpreadSheet:
    @classmethod
    def get_client(cls):
        if os.environ.get("IS_LOCAL", "").lower() == "true":
            creds = GoogleDriveAuth.get_credentials(
                os.environ.get("CLIENT_ID"), os.environ.get("CLIENT_SECRET")  # type: ignore
            )
            ssc = gspread.authorize(creds)  # type: ignore
        else:  # in the cloud
            ssc = gspread.service_account()  # type: ignore
        return ssc


if __name__ == "__main__":
    GoogleDriveAuth.get_credentials(
        os.environ.get("CLIENT_ID"), os.environ.get("CLIENT_SECRET")  # type: ignore
    )

    client = GoogleSpreadSheet.get_client()
    ssid = os.getenv("DRIVE_SS_ID")
    if not ssid:
        raise ValueError("DRIVE_SS_ID is not set.")
    sheet = client.open_by_key(ssid).worksheet("data")
    from gspread_dataframe import get_as_dataframe

    df = get_as_dataframe(sheet)
    print(df)
