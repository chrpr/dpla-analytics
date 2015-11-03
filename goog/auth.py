#!/usr/bin/python

# import required classes
import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

# Declare constants and set configuration values

# The file with the OAuth 2.0 Client details for authentication and authorization.
CLIENT_SECRETS = 'client_secrets.json'

# A helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = '%s is missing' % CLIENT_SECRETS

# The Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics.readonly',
    message=MISSING_CLIENT_SECRETS_MESSAGE)

# A file to store the access token
TOKEN_FILE_NAME = 'analytics.dat'

def prepare_credentials():
  # Retrieve existing credendials
  storage = Storage(TOKEN_FILE_NAME)
  credentials = storage.get()

  # If existing credentials are invalid and Run Auth flow
  # the run method will store any new credentials
  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage) #run Auth Flow and store credentials

  return credentials

def initialize_service():
  http = httplib2.Http()

  #Get stored credentials or run the Auth Flow if none are found
  credentials = prepare_credentials()
  http = credentials.authorize(http)

  #Construct and return the authorized Analytics Service Object
  return build('analytics', 'v3', http=http)