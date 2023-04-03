from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes required for your application
scopes = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/forms']

# Set up the OAuth2 flow for your application
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=scopes)
credentials = flow.run_local_server(port=0)

# Save the credentials for future use
with open('token.json', 'w') as token:
    token.write(credentials.to_json())