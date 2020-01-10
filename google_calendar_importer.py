from __future__ import print_function
from config import Config
import google_calendar_util
from datetime import datetime
import sys

config_file_loc = "config.json"
verbose = False
write_to_cal = True
future_only = False
now = None

def init():
    p("Reading configuration...")
    config = Config().from_json_file(config_file_loc)
    p("Initializing Pointstreak Teams")
    config.init_pointstreak_teams()
    #config.init_ics_teams()
    return config;

def create_calendar(config):
    defaultCalendar = config.defaultCalendarName
    cleared_calendars = []
    service = None
    for psTeam in config.pointstreakTeams :
        #initialize the ID to be default.
        if write_to_cal:
            if( service == None ):
                service = google_calendar_util.get_service()
            p("Writing games to google calendar...")
            cal_id = google_calendar_util.get_calendar_id( service, psTeam, defaultCalendar )
            #right now we just clear whole thing first then add items.
            if cal_id not in cleared_calendars:
                #only clear once, though
                p("Clearing all events from calendar:"+cal_id);
                clear_calendar(service, cal_id)
                cleared_calendars.append(cal_id)
            p("Writing {} games to schedule.".format(len(psTeam.schedule.games)))
            for game in psTeam.schedule.games:
                write_game = True
                if future_only:
                    write_game = check_future_date(game.startdate)
                if write_game:   
                    google_calendar_util.insert_new_event(service,cal_id,game.to_calendar_event())
                if verbose:
                    print(game.to_calendar_event())

def check_future_date(date):
    if date < now:
        return False
    else:
        return True

def clear_calendar(service,cal_id):
    events = google_calendar_util.get_cal_events(service,cal_id)
    for event in events :
        service.events().delete(calendarId=cal_id,eventId=event.get("id")).execute();

def create_csv():
    return ""
    
def p(string):
    if verbose:
        print(string+ "\n")


if __name__ == '__main__':
    config = init()
    now = datetime.now()

    if "--test" in sys.argv:
        write_to_cal = False
    if "--verbose" in sys.argv:
        verbose = True
    if "--future-only" in sys.argv:
        future_only = True
    create_calendar(config)

