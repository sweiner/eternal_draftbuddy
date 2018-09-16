from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import sys
import os

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1NH1i_nfPKhXO53uKYgJYICrTx_XSqDC88b2I3e0vsc0'
RANGE_NAME = 'Tabulated Summary+Thoughts!A:K'
HEADER_RANGE = 'Tabulated Summary+Thoughts!A2:K2'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

try:
    if os.environ['PRODUCTION'] == True:
        TOKEN_PATH = os.path.normpath('/home/atraeus/eternal_draftbuddy/token.json')
        CRED_PATH = os.path.normpath('/home/atraeus/eternal_draftbuddy/credentials.json')
    else:
        TOKEN_PATH = os.path.join(THIS_FOLDER, 'token.json')
        CRED_PATH = os.path.join(THIS_FOLDER,'credentials.json')
except KeyError as e:
    TOKEN_PATH = os.path.join(THIS_FOLDER, 'token.json')
    CRED_PATH = os.path.join(THIS_FOLDER,'credentials.json')

def get_tdc_info():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage(TOKEN_PATH)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CRED_PATH, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    header = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=HEADER_RANGE).execute()
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    header_values = header.get('values', [])
    data_values = result.get('values', [])

    if not header_values or not data_values:
        print('No data found.')
    else:
        return header_values,data_values

if __name__ == '__main__':
    get_tdc_info()