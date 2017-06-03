import gspread
import pytz
import program.wsgi
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from gsheet.models import Session, Speaker, Staff, Room
import ipdb


def parse_time(timestr):
    time = datetime.strptime(timestr, '%m/%d/%Y %H:%M:%S')
    return pytz.utc.localize(time)


def parse_confirm(confirm_str):
    true_str = ['True', '1', 'Y', 'y', 'Yes', 'yes']
    return confirm_str in true_str


def read_program(sheet):
    wks = sheet.worksheet('ProgramData')
    # data is a list of dictionaries, where the keys are headers.
    data = wks.get_all_records()
    count = len(data)
    # Speaker.objects.all().delete()
    # Session.objects.all().delete()

    for i in range(count):
        if data[i]['Start_datetime'] == '':
            continue
        # try to retrieve the session by name (Topic)
        # or creat a new instance if not exist
        session, created = Session.objects.get_or_create(
            name=data[i]['Topic'],
            startTime=parse_time(data[i]['Start_datetime']))

        session.startTime = parse_time(data[i]['Start_datetime'])
        session.endTime = parse_time(data[i]['End_datetime'])
        session.name = data[i]['Topic']
        session.slot = data[i]['Slot']
        session.parallelOrder = data[i][
            'Parallel'] if data[i]['Parallel'] != '' else 0
        session.confirmed = parse_confirm(data[i]['Confirmed'])
        session.save()

        # Speakers:
        for j in range(5):
            speakerName = data[i]['Speaker ' + str(j+1)]
            if speakerName == '':
                continue
            try:
                speaker = Speaker.objects.get(name=speakerName)
            except:
                speaker = Speaker.objects.create(name=speakerName)
                speaker.save()

            if speaker not in session.Speakers.all():
                session.Speakers.add(speaker)


def read_speaker(sheet):
    wks = sheet.worksheet('Speaker data')
    data = wks.get_all_records()
    count = len(data)

    for i in range(count):
        speakerName = data[i]['Name']
        if speakerName == '':
            continue

        try:
            speaker = Speaker.objects.get(name=speakerName)
            speaker.introduction = data[i]['Introduction']
            speaker.affliation = data[i]['Affliation']
            speaker.registered = parse_confirm(data[i]['Registered'])
            speaker.save()
        except:
            print(speakerName)


def earliest_session(speaker):
    start_times = [session.startTime for session in speaker.sessions.all()]
    return min(start_times)


def write_speaker(sheet):
    target_wks = sheet.worksheet('SpeakerData')
    headers = ['ID', 'Name', 'Session 1', 'Session 2', 'Session 3',
               'Session 4', 'Earliest Time', 'Introduction', 'Registered',
               'Contact_Staff', 'Confirmed']
    target_wks.insert_row(headers, 1)
    index = 2
    cells_to_update = []
    for speaker in Speaker.objects.all():
        print("working on speaker: ", speaker.name)
        celllist = target_wks.range(index, 1, index, 11)
        celllist[0] = speaker.id
        celllist[1] = speaker.name
        sessions = [session.name for session in speaker.sessions.all()]
        num_sessions = len(sessions)
        celllist[2:6] = sessions + [''] * (4 - num_sessions)
        celllist[6] = earliest_session(speaker)
        celllist[7] = speaker.introduction
        celllist[8] = speaker.registered
        contact_staff = speaker.contact_staff
        celllist[9] = '' if contact_staff is None else speaker.contact_staff.name
        celllist[10] = speaker.confirmed
        cells_to_update += celllist
        index += 1


def main():

    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'service_credential.json', scope)
    client = gspread.authorize(creds)

    spreadsheetId = '1AaiKWlsIx9mwawXIV0qFIBFTm3ap2uQqlILGNcmhtnw'
    sheet = client.open_by_key(spreadsheetId)
    read_program(sheet)
    read_speaker(sheet)
    # write_speaker(sheet)


if __name__ == '__main__':
    main()
