import UPL.Core as cr
import sqlite3

def sql_version():
	return sqlite3.version

class sqlDB:
	def __init__(self, db_file):
		self.db_file = db_file
		self.sql_cmd = [] 
	
	def init_sql(self):
		try:
			self.con = sqlite3.connect(self.db_file)
		except sqlite3.Error as error:
			return error

	def sql_load(self):
		print("Input values with '~' depicting new char")
		self.sql_cmd = cr.ainput(prompt="SQL Command> ", outType=list, delim="~")
		
		

	def sql_table(self):
		cur = con.cursor()

		sql_cmd = cr.ainput(prompt="SQL Command> ", outType=str)

		try:
			cur.execute(self.sql_cmd)

		except sqlite3.Error as error:
			return error

		finally:
			con.commit()	