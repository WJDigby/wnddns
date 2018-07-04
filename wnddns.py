from apiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
import os.path

SENDER = <sender>
RECIPIENT = <recipient>
SUBJECT = <subject>
CONTENT = <content>
SCOPE = 'https://www.googleapis.com/auth/gmail.compose' # Allows sending only, not reading

# Initialize the object for the Gmail API
# https://developers.google.com/gmail/api/quickstart/python
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPE)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))


def get_current_ip():
    resp, content = Http().request("https://api.ipify.org?format=text", "GET")
    current_ip = content.decode().rstrip()

    if os.path.isfile('ip.txt'):
        f = open('ip.txt', 'r')
        previous_ip = f.read().rstrip()
        f.close()
    else:
        f = open('ip.txt', 'w')
        f.write(current_ip)
        f.close()
        previous_ip = current_ip

    return current_ip, previous_ip

# https://developers.google.com/gmail/api/guides/sending
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


# https://developers.google.com/gmail/api/guides/sending
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
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)



current_ip, previous_ip = get_current_ip()
if current_ip != previous_ip:
    raw_msg = create_message(SENDER, RECIPIENT, SUBJECT, CONTENT)
    send_message(service, "me", raw_msg)
