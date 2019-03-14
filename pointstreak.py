from __future__ import print_function
from bs4 import BeautifulSoup
from datetime import datetime
from calendar_event import CalendarEvent
import urllib.request
import re

DEFAULT_GAME_LENGTH = 90#IN MINUTES
SEASON_REGEX = '[^\d]*(\d{4})([-](\d{4}))?'
SEASON_SELECTOR = "font.season"
GAME_TABLE_IDENTIFIER = "table.nova-stats-table tr"
ROWS = ["Home","Away","Rink","Date","Time"]

POINTSTREAK_URL = "http://stats.pointstreak.com/players/print/players-team-schedule.html?teamid={0}&seasonid={1}"

class PointstreakTeam:
	teamId = None
	seasonId = None
	schedule = None
	calendarName = None
	calendarId = None
	nameReplacements = None

	def get_url(self):
		return POINTSTREAK_URL.format(self.teamId,self.seasonId);
	def from_json_obj(self,json_obj):
		pointstreakTeam = self;
		pointstreakTeam.nameReplacements = json_obj["nameReplacements"];
		if( json_obj.get("calendarId") == None):
			pointstreakTeam.calendarName = json_obj["calendarName"] 
		pointstreakTeam.teamId = json_obj["teamId"]
		pointstreakTeam.seasonId = json_obj["seasonId"]
		pointstreakTeam.schedule = PointstreakTeamSchedule().init_from_team(self);
		return pointstreakTeam;

	def to_string(self):
		return "Team: {}\nTeamID: {} \nSeasonId: {}\nSchedule: {}".format(self.get_url(),self.teamId,self.seasonId,self.schedule);

class PointstreakTeamSchedule:
	htmlSoup = None
	games = []
	startyear = None
	endyear = None
	team = None

	def init_from_team(self,team):
		self.team = team;
		self.get_page_source();
		return self;
	def get_page_source(self):
		self.htmlSoup = BeautifulSoup(urllib.request.urlopen(self.team.get_url()).read(),'html.parser');
		self.get_season_info()
		self.get_game_list()
	def get_season_info(self):
		gameSeason = self.htmlSoup.select(SEASON_SELECTOR)
		if( gameSeason and len(gameSeason) == 1 ):
			pattern = re.compile(SEASON_REGEX)
			match = pattern.match(gameSeason[0].string)
			if( match and match.group(2)):
				#winter season, 2 years
				self.startyear = match.group(1)
				self.endyear = match.group(3)
			elif (match and match.group(1) ):
				self.startyear = match.group(1)
				self.endyear = match.group(1)	


	def get_game_list(self):
		gameRows = self.htmlSoup.select(GAME_TABLE_IDENTIFIER);
		for row in gameRows:
			tds = row.find_all("td")
			if( len(tds) >= len(ROWS)):
				game = PointStreakGame();
				game.home = self.translate_team_name(tds[0].a.string)
				game.away = self.translate_team_name(tds[1].a.string)
				tmp = tds[4].find_all("a");
				game.rink = tmp[0].string
				game.gamesheet = tmp[1]["href"]
				date = tds[2].string
				time = tds[3].string
				gameYear = self.startyear;
				game.startdate = datetime.strptime(date + " "+str(self.startyear)+" " + time, '%a, %b %d %Y %I:%M %p')
				if( self.endyear != self.startyear and game.startdate.month >= 1 and game.startdate.month <= 4):
					game.startdate = datetime.strptime(date + " "+str(self.endyear)+" " + time, '%a, %b %d %Y %I:%M %p')
				self.games.append(game);
		return

	def translate_team_name(self,oldName):
		newName = oldName
		for replaceName,regex in self.team.nameReplacements.items():
				regex = re.compile(regex)
				if regex.match(oldName):
					newName = replaceName
					break
		return newName

	def as_calendar_event_list(self):
		event_list = []
		for game in self.games:
			event_list.append(game.to_calendar_event());
		return event_list;

	def init(self,url):
		self.webpage_url = url;
		get_page_source();
		get_game_list();

class PointStreakGame:
	home=None
	away=None
	rink=None
	startdate=None
	gamesheet=None

	def to_calendar_event(self):
		#create_event_object(event_name,startdate,timezone='America/Los_Angeles',enddate=None,event_location="",event_description=""):
		return CalendarEvent.create_event_object(
			event_name = self.away + " @ " + self.home,
			startdate = self.startdate,
			event_location = self.rink,
			event_description = self.gamesheet,
			length = DEFAULT_GAME_LENGTH
			);

	def to_string(self):
		return "Home:"+str(self.home)+"\nAway:"+str(self.away)+"\nDate:"+str(self.startdate)+"\nRink:"+str(self.rink)+"\nGamesheetUrl:"+str(self.gamesheet)+"\r\n\n";

