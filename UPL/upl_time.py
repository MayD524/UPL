from math import isclose
import datetime

class upl_time:

	def upl_timestamp():
		now = datetime.datetime.now()
		return datetime.timestamp(now)


	def date_comp(t2, date_format="%Y-%m-%d"):
		"""
		t1 should be the current date
		t2 should be preformatted 

		Just checks if the date is correct (will not check for time difference)
		"""
		t1 = datetime.datetime.now().strftime(date_format)

		if t1 == t2:
			return True

		else:
			return False

	def min_close(comp, const, difference):
		"""
		Input should be %H:%m
		returns true if comp time is within const time
		comp - "now"
		const - the static time we are compairing agains
		difference - the max +- difference that will result in 
		returning True
		"""
		if comp == const:
			return True

		comp = comp.split(":")
		const = const.split(":")
		if int(comp[1]) + difference >= 60:
			comp[1] = (int(comp[1]) + difference) - 60
			comp[0] = int(comp[0]) + 1

		if int(comp[0]) == int(const[0]):
			if isclose(int(comp[1]), int(const[1]), rel_tol=difference):
				return True

		return False

