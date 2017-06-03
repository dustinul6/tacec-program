from __future__ import print_function
import httplib2
import program.wsgi
import os
import pytz
import ipdb
import gspread

from df2gspread import gspread2df as g2d
from gsheet.models import Session, Room, Speaker, Staff
from datetime import datetime
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(
        credential_dir,
        'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def parse_time(timestr):
    time = datetime.strptime(timestr, '%m/%d/%Y %H:%M:%S')
    return pytz.utc.localize(time)


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1AaiKWlsIx9mwawXIV0qFIBFTm3ap2uQqlILGNcmhtnw'
    rangeName = 'ProgramData!A2:T'
    # dateTimeRenderOption=SERIAL_NUMBER
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    sheetName = 'ProgramData'
    df = g2d.download(
        spreadsheetId,
        sheetName,
        col_names=True)


    print(df)

    values = result.get('values', [])

    # if not values:
        # print('No data found.')
    # else:
        # for row in :
            # print(row)
            # if row[3] == '':
                # continue

            # if row[8] == '':
                # row[8] = 0

            # session = Session(
                # name=row[9],
                # startTime=parse_time(row[5]),
                # endTime=parse_time(row[6]),
                # slot=row[7],
                # parallelOrder=row[8],
                # room=row[10]
                # )
            # for k in range(5):
                # speakerName = row[11]
                # try:
                    # speaker = Speaker.objects.get(name=speakerName)
                # except ObjectDoesNotExist:
                    # speaker = Speaker.objects.create(name=speakerName)

                # session.Speakers.add(speaker)
            # print(
                # session.startTime,
                # session.endTime,
                # session.slot,
                # session.parallelOrder)
            # session.save()
            # # Print columns A and E, which correspond to indices 0 and 4.


if __name__ == '__main__':
    main()
