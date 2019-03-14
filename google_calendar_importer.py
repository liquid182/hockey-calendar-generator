from __future__ import print_function
from config import Config
import google_calendar_util


config_file_loc = "config.json"

def init():
    config = Config().from_json_file(config_file_loc)
    config.init_pointstreak_teams()
    #jconfig.init_ics_teams()
    return config;

def create_calendar(config):
    service = google_calendar_util.get_service()
    defaultCalendar = config.defaultCalendarName
    cleared_calendars = []
    for psTeam in config.pointstreakTeams :
        #initialize the ID to be default.
        cal_id = google_calendar_util.get_calendar_id( service, psTeam, defaultCalendar )
        #right now we just clear whole thing first then add items.
        if cal_id not in cleared_calendars:
            #only clear once, though
            clear_calendar(service, cal_id)
            cleared_calendars.append(cal_id)
        games = psTeam.schedule.as_calendar_event_list()
        for game in games:
            google_calendar_util.insert_new_event(service,cal_id,game)

def clear_calendar(service,cal_id):
    events = google_calendar_util.get_cal_events(service,cal_id)
    for event in events :
        service.events().delete(calendarId=cal_id,eventId=event.get("id")).execute();

def create_csv():
    return ""
    
if __name__ == '__main__':
    config = init()
    create_calendar(config)
