from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from base64 import urlsafe_b64encode
from apiclient import errors
import requests
import json
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_message = urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_message.decode()}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId="me", body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print(error)


def get_ip():
    ips = {}
    ips['new'] = "new"
    ips['old'] = "old"
    if os.path.exists('/ips.json'):
        with open('/ips.json') as f:
            ips = json.load(f)
            response = requests.get("https://api.ipify.org?format=json")
            resApi = response.json()
            if ips['new'] == resApi['ip']:
                print("Las ips son iguales")
                return 0
            else:
                print("Nueva ip detectada, actualizando..")
                ips['old'] = ips['new']
                ips['new'] = resApi['ip']
                with open('/ips.json', 'w') as json_file:
                    json.dump(ips, json_file)
                return resApi['ip']
    else:
        with open('/ips.json', 'w') as outfile:
            json.dump(ips, outfile)
        return 0


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/token.json'):
        creds = Credentials.from_authorized_user_file('/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    ip = get_ip()
    if (ip != 0):
        message = create_message(
            ' /* HERE GOES THE THE SENDER EMAIL */ ', ' /* HERE GOES THE THE RECEIVER EMAIL */ ', 'You have a new public IP!', "Your new IP is : "+ip)
        send_message(service, "me", message)


if __name__ == '__main__':
    main()
