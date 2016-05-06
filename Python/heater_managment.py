import os, csv, time, math
import datetime as dt
import numpy as np
import pandas as pd
from sympy.solvers import solve
from sympy import Symbol
absolute_path_py = "/Users/nicolasbadoux/Box\ Sync/CMU/Semestre\ 2/Green\ Computing/Project/Programming/"
absolute_path_wemo = "/Users/nicolasbadoux/Documents/WemoSafe/"
absolute_path_oregon = ""

T_SLEEP = 180 # seconds
my_FMT = '%Y-%m-%d %H:%M:%S';
SET_TEMP = 25
VALID_RANGE = 2


def get_last_line():
	csv_filename = "temperatures_formatted.csv"#absolute_path_py + "temperatures_formatted.csv"
	with open(csv_filename,'rb') as f:
	    reader = csv.reader(f, delimiter=';')
	    lastline = reader.next()
	    for line in reader:
	        lastline = line
	    return lastline

def fix_temp():
	print "Keeping the room in the desired temperature range."

	act_val = get_last_line()
	act_temp = float(act_val[3])
	state = int(act_val[4])

	if act_temp < SET_TEMP and state != 1:
		os.system("python " + absolute_path_wemo + "wemo_on.py")
	elif act_temp > SET_TEMP + VALID_RANGE and state == 1:
		os.system("python " + absolute_path_wemo + "wemo_off.py")
	else:
		print "good range"


def weather_prep(delta):
	# delta in min

	with open("weather_forecast.txt") as w_file:
		weather_time = list()
		weather_temp = list()
		for s in w_file.readlines():
			weather_time.append(dt.datetime.strptime(s[0:19], "%Y-%m-%d %H:%M:%S"))
			weather_temp.append(int(s[20:22]))
		now = dt.datetime.now().replace(second=0)+dt.timedelta(minutes=1)
		index = list()
		forecast = list()
		for i in range(0,delta):
			indexing = now + dt.timedelta(minutes=i)
			index.append(indexing)
			clostest_temp = weather_temp[min(range(len(weather_time)), key=lambda x:abs(weather_time[x] - indexing))]
			forecast.append(clostest_temp)
		return pd.Series(forecast, index=index)


def reactivate (delta):
	os.system("python " + absolute_path_py + "weather.py")
	print "Looking for a reactivation in "+str(delta)+" minutes"
	act_val = get_last_line()
	print "Actual values"+str(act_val)

	act_room = float(act_val[3])
	act_appart = float(act_val[1])
	coeff = [[0.0332,-0.0695,0.2021], 
	[0.0654, -0.0840, 0.4108],
    [0.0964, -0.0927, 0.6081],
    [0.1258, -0.0980, 0.7942],
    [0.1540, -0.1010, 0.9721],
    [0.1809, -0.1021, 1.1420],
    [0.2066, -0.1020, 1.3050],
    [0.2312, -0.1012, 1.4618],
    [0.2550, -0.1003, 1.6132],
    [0.2778, -0.0992, 1.7593],
    [0.2997, -0.0977, 1.9001],
    [0.3206, -0.0961, 2.0361],
    [0.3407, -0.0943, 2.1676],
    [0.3597, -0.0921, 2.2942],
    [0.3779, -0.0897, 2.4165],
    [0.3954, -0.0874, 2.5356],
    [0.4125, -0.0852, 2.6517],
    [0.4292, -0.0832, 2.7651],
    [0.4454, -0.0815, 2.8755],
    [0.4610, -0.0798, 2.9827],
    [0.4761, -0.0782, 3.0869],
    [0.4908, -0.0767, 3.1882],
    [0.5049, -0.0753, 3.2863],
    [0.5186, -0.0741, 3.3819],
    [0.5318, -0.0728, 3.4747],
    [0.5446, -0.0715, 3.5649],
    [0.5567, -0.0701, 3.6521],
    [0.5682, -0.0686, 3.7366],
    [0.5793, -0.0673, 3.8185],
    [0.5901, -0.0661, 3.8980]]
	outside = weather_prep(delta)
	outside_agg = (outside - act_room).sum()/1000
	appart_diff = act_appart - act_room
	x = Symbol('x')
	eq = act_room + coeff[delta/10][0] * appart_diff + coeff[delta/10][1] * outside_agg + coeff[delta/10][2] * x - SET_TEMP
	res = solve(eq, x)
	print "we need to run the heater for "+str(int(res[0]*delta))
	if delta < 15 or res[0] > delta/(delta-10)-0.05:
		# 0.05 margin
		# the heater should be running

		fix_temp() # start 




def main():

	while True:
		#os.system("cp " + absolute_path_oregon + "example2.csv" + absolute_path_py)
		#os.system("cp " + absolute_path_wemo + "data.csv" + absolute_path_py)
		#os.system("python " + absolute_path_py + "parser_uniform.py")
		#os.system("python " + absolute_path_py + "presence.py")
		
		
		with open("next_alarm.txt", 'r') as alarm_file:
			late_wake_up = dt.time(hour = 12, minute=30)
			early_wake_up = dt.time(hour=3)

			alarm = alarm_file.read()
			next_alarm = None
			# foramt = Fri Apr 22 09:30:00 EDT 2016
			if not "none" in alarm:
				next_alarm = dt.datetime.strptime(alarm, "%a %b %d %H:%M:%S %Z %Y")
			sleeping = False
			now = dt.datetime.now()
			if next_alarm != None:
				if now.time() > late_wake_up:
					# time is next day 
					day = dt.datetime.today()+ dt.timedelta(1)
					print day
					if next_alarm > dt.datetime.combine(day,early_wake_up) and next_alarm < dt.datetime.combine(day,late_wake_up):
						sleeping = True #if alarm set, and is scheduled between 3 AM and 12H30
				else:
					# in the morning
					day = dt.datetime.today()
					if next_alarm > dt.datetime.combine(day,early_wake_up) and next_alarm < dt.datetime.combine(day,late_wake_up):
						sleeping = True #if alarm set, and is scheduled between 3 AM and 12H30

		with open("heater_command.txt", 'r') as command_file:
			commands = command_file.read()
			present = "Present = True" in commands
			index_date = commands.index("Reactivate at = ") + len("Reactivate at = ")
			if (present or commands[index_date:index_date+4] == "None") and not sleeping: # keep temperature in range
				fix_temp()
			else:
				# we can adjust the heater
				if commands[index_date:index_date+4] == "None":
					date_reac = next_alarm
				else:
					date_reac = dt.datetime.strptime(commands[index_date:index_date+18], my_FMT) # 18 = len(date_string)

				dist = int((date_reac - dt.datetime.now()).seconds/600.0*10)
				if dist <= 300: # max 6h in advance
					reactivate(dist)
				else:
					print "Too far away form time of return, no startup scheduled."


		time.sleep(T_SLEEP) 


if __name__ == '__main__':
    main()
