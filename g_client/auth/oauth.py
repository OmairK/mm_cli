from os import path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

DEFAULT_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate(token_file, scopes=DEFAULT_SCOPES):
    """
    Handles authentication workflow for accessing google apps
    """

    creds = None
    if path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds

    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", scopes
        )
        creds = flow.run_local_server()
        with open(token_file, "x") as tf:
            tf.write(creds.to_json())
        return creds
