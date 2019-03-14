## Installation

```pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```

## Setup

Modify config.json to match your teams information

## Configs
Sample Config:
```json
{
  "defaultCalendarName":"RM Hockey TEST",
  "defaultCsvFileName": "~/Downloads/Hockey.csv",
  "sourceIcsUrls": [
    {
      "url":"",
      "calendarName":"",
      "nameReplacements":{
        "A La Mode":"^.*A[-\\s]+La[-\\s]+Mode.*$"
      }
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
      "calendarName": "RM Hockey TEST"
    }
}
```

_**Note: If a Calendar ID is provided,the Calendar Name will be ignored.**_

### defaultCalendarName 
Name of your google calendar to import events into (If no configuration is found on your calendar config directly)

### defaultCalendarId
ID of your google calendar to import events into  (If no configuration is found on your calendar config directly)

### nameReplacements
A dictionary of "name":"expression" pairs used to replace team names which are misspelt.  Can support regular expressions or exact strings in value, the key is expected to be the replacement value.  Will work on both home and away teams.  For example, both the following are valid:
```json
"A La Mode":"^.*A[-\\s]+La[-\\s]+Mode.*$",
"Da Toads":"Da Todes"
```
The former will check the string to see if it matches the provided regular expression, and if it matches, replaces the original with "A La Mode".  The latter is simpler, where it will substitute "Da Toads" if the original is spelt "Da Todes".

### sourceIcsUrls 
Array of an ICS calendar.  Expected format to match bench.ashl.com. Required to provide the url property.
#### url
Fully Qualified URL of the schedule's ICS in question
### pointstreakTeams
Array of pointstreak teams.  Required to provide teamId, seasonId (found in the url of pointstreak team page)
#### teamId
Team Identifier as seen within the pointstreak teams homepage URL (`&teamId=<teamId>`)
#### seasonId
Team Identifier as seen within the pointstreak teams homepage URL (`&seasonId=<seasonId>`)

## Run

```python3 google_calendar_importer.py```
By default the above will parse all teams and write to the configured calendar (if found)

Runtime Arguments:

```--verbose```
Write some additional log statements.

```--test```
Will not write anything to calendar, instead print events to screen.

```--future-only``` 
Will only get games that haven't already happened.

Given the above, the following would do a test run of future games provided in the config:

```python3 google_calendar_importer.py --test --future-only```

