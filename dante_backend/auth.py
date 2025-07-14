import os
import msal
from dotenv import load_dotenv

load_dotenv(dotenv_path='dante_backend/.env')

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"
SCOPES = ["Mail.ReadWrite"]
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/callback")

msal_app = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
)

def get_auth_url():
    return msal_app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def get_token_from_code(auth_code):
    result = msal_app.acquire_token_by_authorization_code(
        code=auth_code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    return result
