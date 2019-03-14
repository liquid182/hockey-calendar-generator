from __future__ import print_function
from pointstreak import PointstreakTeam
import json
import os.path

class Config:
	sourceIcsUrls = []
	configJson = {}
	calendarName = None
	pointstreakTeams = []
	def from_json_file(self,json_file_path):
		config = self
		if os.path.exists(json_file_path):
			with open(json_file_path, 'rb') as json_file:
				config.configJson = json.load(json_file)
		if not config.configJson:
			print("No configuration file found in "+ json_file_path);           
			return None
		config.sourceIcsUrls = config.configJson["sourceIcsUrls"];
		config.defaultCalendarName = config.configJson["defaultCalendarName"]
		return config;

	def init_pointstreak_teams(self):
		for pointstreakTeamObj in self.configJson["pointstreakTeams"]:
			self.pointstreakTeams.append(PointstreakTeam().from_json_obj(pointstreakTeamObj));
		return self;

	def to_string(self):
		return str(self.pointstreakTeams[0].to_string());

