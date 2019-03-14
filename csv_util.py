from __future__ import print_function
import os.path
#
types = ["GAME","SCRIMMAGE","PRACTICE","EVENT"]
game_types = ["PRE-SEASON","REGULAR","PLAYOFF","TOURNAMENT"]

#[Type,Game Type,Title (Optional),Home,Away,Date,Time,Location (Optional),Address (Optional),Notes (Optional)]
class CSV:
	file = None
	fileContents = ""
	filePath = None
	def add_entry(home,away,datetime,title="",location="",address="",notes="",type="GAME",game_type="REGULAR"):
		time = datetime.time();
		date = datetime.date();
		fileContents += "%s,%s,%s,%s,%s,%s,%s,%s,%s\n".format(type,game_type,title,home,away,date,time,location,address,notes);
		return 
	def write_to_file():
		return