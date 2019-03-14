**Installation:**

pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

**Setup**

Modify config.json to match your teams information

**Configs**
Sample Config:
{
  "defaultCalendarName":"RM Hockey TEST",
  "defaultCsvFileName": "~/Downloads/Hockey.csv",
  "sourceIcsUrls": [
    {
      "url":"",
      "calendarName":""
    }
  ],
  "pointstreakTeams": 
    {
      "nameReplacements":
      { 
        "A La Mode":"^.*A[-\\s]+La[-\\s]+Mode.*$"
      },
      "teamId": 725612,
      "seasonId": 18707,
      "calendarName": "RM Hockey TEST",
      "csvFileName": "~/Downloads/A-La-Mode.csv"
    }
}

* If a Calendar ID is provided,the Calendar Name will be ignored.

defaultCalendarName: Name of your google calendar to import events into (If no configuration is found on your calendar config directly)
defaultCalendarId: ID of your google calendar to import events into  (If no configuration is found on your calendar config directly)
sourceIcsUrls: Array 

**Run**

python3 google_calendar_importer.py


