#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from bs4 import BeautifulSoup
import urllib.request



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except:
    flags = None
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def htmlPlan():
    html = urllib.request.urlopen('http://planzajec.uek.krakow.pl/index.php?typ=G&id=100821&okres=1')
    return html

def main(day):
    # type: () -> object
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    try:
        event = service.events().insert(calendarId='primary', body=lesson(day)).execute()
    except:
        pass

    'Event created: %s' % (event.get('htmlLink'))

def actualEvents():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Zbieranie 10 wydarzen..')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def dataGen():
    html=htmlPlan()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")

    # The first tr contains the field names.
    headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]


    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
        datasets.append(dataset)
    #for lesson in datasets:
    #    l+=1
    #    for name in headings:
    #        print(name+':',lesson.get(name))
    #    print("####################")
    #print(datasets[1])
    return datasets

def lesson(day):
    datasets=dataGen()

    start=(datasets[day].get("Termin")+"T"+datasets[day].get("Dzień, godzina")[3:8]+":00+01:00")
    end=(datasets[day].get("Termin")+"T"+datasets[day].get("Dzień, godzina")[11:16]+":00+01:00")

    event = {
        'summary': datasets[day].get("Przedmiot"),
        'location':  datasets[day].get("Sala"),
        'description': datasets[day].get("Typ")+" "+datasets[day].get("Nauczyciel"),
        'start': {
            'dateTime': start,
        },
        'end': {
            'dateTime': end,
        },
    }
    return event


if __name__ == '__main__':
    for day in range(len(dataGen())):
       try:
           main(day)
           print("Dodano wydarzenie "+" ' "+dataGen()[day].get("Przedmiot")+"' ")
       except:
           print("Nie udało się dodać lekcji nr."+" ' "+dataGen()[day].get("Termin")+"' ")
           pass
    #print(lesson(2))
