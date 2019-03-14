import datetime

class CalendarEvent:

    def create_event_object(name,startdate,timezone='America/Los_Angeles',enddate=None,length=60,location="",description=""):
        if(enddate == None and length != None):
            enddate = startdate + datetime.timedelta(0,length*60)
        return  {
                    'summary': name,
                    'location': location,
                    'description': description,
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