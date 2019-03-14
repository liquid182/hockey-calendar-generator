from __future__ import print_function
import datetime
import sys
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

DEFAULT_EVENT_LENGTH = 90#IN MINUTES

def get_service():
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
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service
    
def get_cal_id_from_name(service,name):
    cal_id = None 
    try:
        calendar_list = service.calendarList().list().execute();
        for calendar in calendar_list.get('items',[]):
            if( calendar.get('summary') == name):
                cal_id = calendar.get("id")
    except:
        e = sys.exc_info()[0]
        print("Unable to get calendar with name:"+name+":\n"+str(e))
    return cal_id
def insert_event_list(service,cal_id,events):
    eventIds = []
    for event in events:
        event_obj = service.events().insert(calendarId=cal_id, body=event).execute();
        eventIds.append(event_obj['id'])
    return eventIds;

def insert_new_event(service, cal_id,event):
    event = service.events().insert(calendarId=cal_id, body=event).execute()
    return event['id']

def create_event(service,event,cal_id):
    gEvent = service.events().insert(calendarId=cal_id,body=event).execute()
    return gEvent;

def get_cal_events(service, cal_id):
    events = []
    try:
        events_result = service.events().list(calendarId=cal_id,
                                       maxResults=100, singleEvents=True,
                                       orderBy='startTime').execute()
        events = events_result.get('items',[])
    except:
        e = sys.exc_info()[0]
        print("Unable to get events for calendar [ "+cal_id+"]:\n"+str(e));

    return events;

def get_calendar_id(service,psTeam,defaultCalendarName=None):
        cal_id = None
        if( psTeam.calendarId != None ):
            cal_id = psTeam.calendarId;
        elif ( psTeam.calendarId == None and psTeam.calendarName != None ):
            #if the team didn't provide the ID and did provide the name, do a search...
            cal_id = get_cal_id_from_name(service,psTeam.calendarName)
        if( cal_id == None and defaultCalendarName!= None):
            #This means the name didn't resolve in the search, or neither ID or NAME was provided.  Use default.
            cal_id = get_cal_id_from_name(service,defaultCalendarName)
        if( cal_id == None):
            if( defaultCalendarName == None):
                defaultCalendarName = "None"
            print("Cannot find Calendar ["+psTeam.calendarName+"] or default ["+defaultCalendarName+"].  Please check spelling and casing of names.")       
        return cal_id;

def print_events(events):
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
