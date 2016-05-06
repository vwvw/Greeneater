
import csv;
import copy
from datetime import datetime,timedelta

DELAY = 60 #seconds between each input
REDUCING_FACTOR = 1; # keep every REDUCING_FACTOR lines, integer
#format date and time: 2016-02-27 01:31:12
my_FMT = '%Y-%m-%d %H:%M:%S';


def device_to_index( d ):
	# 0 = appartment
	# 1 = room
	# 2 = outdoor
	if(d == 'C6'): return 0
	elif(d == '22' or d == '6D' or d == '3A' or d == 'D8'): return 1
	elif(d == '89'): return 2
	else: return -1


ind = open('index_file.txt','w')


with open('data.csv', 'r') as heater_read:
	heater_data = list(csv.reader(heater_read, delimiter=';', quotechar='|'))
#
#
heater_data[0][3] = "0" # state 0 on the first line. because starte recording false
heater_data[0][4] = "0"
#
#

#format date and time: Sat Feb 27 01:35:06 2016
original_FMT = '%a %b %d %H:%M:%S %Y';
heater_FMT = '%d/%m/%Y %H:%M:%S';

grouped = []
new_line = ['2016-01-01 00:00:00','0','0','0','0','0','0']
N_temp = 1
with open('example2.csv', 'r') as csvfile_read:
	data = list(csv.reader(csvfile_read, delimiter=';', quotechar='|'))
	N_temp = len(data)
	i = 0
	for data_line in data:
		i= i+1
		if(i != 1):
			if(i % (N_temp/10) == 0):
				print "Done with converting ", round(i / (N_temp/10))*10,"%"
			if(i % (2 * REDUCING_FACTOR) == 1):
				#format : dateAndTime;device;temperature
				date_time = datetime.strptime(data_line[0], original_FMT);
				device = device_to_index(data_line[1]);
				if device != -1:
					new_line[0] = date_time.strftime(my_FMT)
					temp = data_line[2]
					if temp != '0':	
						new_line[device+1] = temp #update the temperature (index+1 since datetime first)
						grouped.append(copy.deepcopy(new_line))

print i
ind.write("index_temp:"+str(i)+"\n")

print "Done with conversion and arrangment"
print "---------------"

temp = open('temperatures_formatted.csv','w')
temp.write("dateAndTime;appartment;outside;room;state;actual_power;total_power\n")

N_temp = len(grouped)

index_heater = 0

first_date = datetime.strptime(grouped[0][0], my_FMT)
last_date = datetime.strptime(grouped[len(grouped)-1][0], my_FMT)
act_date = first_date - timedelta(0,first_date.second)
i = 1;
while act_date < last_date:
	if i % (N_temp/10) == 0:
		print "Done with resampling ", round(i / (N_temp/10))*10,"%"
	line_i = grouped[i]
	date_i = datetime.strptime(grouped[i][0], my_FMT)
	line_i_smaller = grouped[i-1]
	date_i_smaller = datetime.strptime(grouped[i-1][0], my_FMT)
	if date_i > act_date:
		next_date_heater = datetime.strptime(heater_data[index_heater][0] + " " + heater_data[index_heater][1], heater_FMT)
		last_date_heater = datetime.strptime(heater_data[index_heater-1][0] + " " + heater_data[index_heater-1][1], heater_FMT)
		while next_date_heater < act_date and index_heater + 1 < len(heater_data):
			last_date_heater = next_date_heater
			index_heater = index_heater + 1
			next_date_heater = datetime.strptime(heater_data[index_heater][0] + " " + heater_data[index_heater][1], heater_FMT)

		if next_date_heater - act_date < last_date_heater - act_date:
			closest_heater_line = index_heater
		else:
			closest_heater_line = index_heater -1
		if 	heater_data[closest_heater_line][3] != '1':
			heater_data[closest_heater_line][3] = '0';
		heater_line = [heater_data[closest_heater_line][3], heater_data[closest_heater_line][4], heater_data[closest_heater_line][5]]
		#print heater_line
		if date_i - act_date > act_date - date_i_smaller:
			l = [act_date.strftime(my_FMT), line_i_smaller[1], line_i_smaller[2], line_i_smaller[3]]
			l.extend(heater_line)
		else:
			l = [act_date.strftime(my_FMT), line_i[1],line_i[2],line_i[3]]
			l.extend(heater_line)
		temp.write(';'.join(l)+'\n')
		act_date = act_date + timedelta(0,DELAY)
	else:
		i = i+1
print closest_heater_line
print "Done with resampling"


ind.write("index_heat:"+str(closest_heater_line)+"\n")
ind.close()
temp.close()

