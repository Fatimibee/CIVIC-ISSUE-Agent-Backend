import base64
import os
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Paths for your files - adjusted for your folder structure
# Usually, these live in the root or a 'config' folder
CREDENTIALS_PATH = "credentials.json"
TOKEN_PATH = "token.json"


def get_gmail_service():
    creds = None

    # 1. Check if token.json exists (this stores your login session)
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # 2. If there are no valid credentials, let the user log in or refresh
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This part requires credentials.json to exist
            if not os.path.exists(CREDENTIALS_PATH):
                raise Exception(
                    f"{CREDENTIALS_PATH} not found. Download it from Google Cloud Console."
                )

            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # 3. Save the token for the next run so we don't have to log in again
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def sendEmail(to, replyTo, subject, body, image_b64):
    try:
        service = get_gmail_service()
        msg = EmailMessage()
        msg.set_content(body)
        msg["To"] = to
        msg["Subject"] = subject
        msg["Reply-To"] = replyTo

        # Process Image Attachment
        if image_b64:
            # Clean base64 string if it contains the data header from the frontend
            if "base64," in image_b64:
                _, image_b64 = image_b64.split("base64,")

            image_data = base64.b64decode(image_b64)
            msg.add_attachment(
                image_data, maintype="image", subtype="jpeg", filename="evidence.jpg"
            )

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    print("Starting Gmail authentication...")
    service = get_gmail_service()
    print("Authentication successful!")