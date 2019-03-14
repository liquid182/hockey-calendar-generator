import datetime

class CalendarEvent:

    def create_event_object(event_name,startdate,timezone='America/Los_Angeles',enddate=None,length=60,event_location="",event_description=""):
        if(enddate == None and length != None):
            enddate = startdate + datetime.timedelta(0,length*60)
        return  {
                    'summary': event_name,
                    'location': event_location,
                    'description': event_description,
                    'start': {
                        'dateTime': startdate.isoformat(),
                        'timeZone': timezone,
                    },
                    'end': {
                        'dateTime': enddate.isoformat(),
                        'timeZone': timezone,
                    },
                    'reminders': {
                        'useDefault': True,
                    }
                }