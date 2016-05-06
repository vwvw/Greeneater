import csv, copy, os,sys
from datetime import datetime,timedelta

DELAY = 60 #seconds between each input
REDUCING_FACTOR = 1; # keep every REDUCING_FACTOR lines, integer
#format date and time: 2016-02-27 01:31:12
my_FMT = '%Y-%m-%d %H:%M:%S';
absolute_path_py = "/home/pi/Desktop/Python/"
absolute_path_wemo = "/home/pi/Desktop/Wemo/"
absolute_path_oregon = "/home/pi/OregonPi/"

#format date and time: Sat Feb 27 01:35:06 2016
original_FMT = '%a %b %d %H:%M:%S %Y';
heater_FMT = '%d/%m/%Y %H:%M:%S';






def get_last_line():
	csv_filename =  "temperatures_formatted.csv"
	with open(csv_filename,'rb') as f:
	    reader = csv.reader(f, delimiter=';')
	    lastline = reader.next()
	    for line in reader:
	        lastline = line
	    return lastline


def device_to_index( d ):
	# 0 = appartment
	# 1 = room
	# 2 = outdoor
	if(d == 'C6'): return 0
	elif(d == '22' or d == '6D' or d == '3A' or d == 'D8'): return 1
	elif(d == '89'): return 2
	else: return -1

def main():
	with open('index_file.txt','r') as index_file:
		line = index_file.readline()
		last_index_temp = int(line.split(":")[1])
		line = index_file.readline()
		last_index_heater = int(line.split(":")[1])


	if last_index_temp % 2 != 0:
		print "false index, remember blank lines..."
		return 

	if last_index_temp > 2:
		last_parsed = get_last_line()
	else:
		last_parsed = ['2016-01-01 00:00:00','0','0','0','0','0','0']
	last_date_parsed = datetime.strptime(last_parsed[0],my_FMT)


	grouped = [last_parsed]
	new_line = last_parsed
	with open('example2.csv', 'r') as csvfile_read:
		data = list(csv.reader(csvfile_read, delimiter=';', quotechar='|'))
		for i in range(last_index_temp,len(data),2):
			data_line = data[i]
			#format : dateAndTime;device;temperature
			date_time = datetime.strptime(data_line[0], original_FMT);
			device = device_to_index(data_line[1]);
			if device != -1:
				new_line[0] = date_time.strftime(my_FMT)
				temp = data_line[2]
				if temp != '0':	
					new_line[device+1] = temp #update the temperature (index+1 since datetime first)
					grouped.append(copy.deepcopy(new_line))
		new_last_index_temp = i

	print "Done with conversion and arrangment"
	print "---------------"

	print new_last_index_temp
	temp = open('temperatures_formatted.csv','a')

	with open('data.csv', 'r') as heater_read:
		heater_data = list(csv.reader(heater_read, delimiter=';', quotechar='|'))


	N_temp = len(grouped)
	N_heater = len(heater_data)

	last_date = datetime.strptime(grouped[N_temp-1][0], my_FMT)
	if last_index_temp == 0:
		first_date = datetime.strptime(grouped[0][0], my_FMT)
		act_date = first_date - timedelta(0,first_date.second)
	else:
		act_date = last_date_parsed + timedelta(0,DELAY)

	index_heater = last_index_heater

	i = 1;
	while act_date < last_date:
		line_i = grouped[i]
		date_i = datetime.strptime(grouped[i][0], my_FMT)
		line_i_smaller = grouped[i-1]
		date_i_smaller = datetime.strptime(grouped[i-1][0], my_FMT)
		if date_i > act_date:
			next_date_heater = datetime.strptime(heater_data[index_heater][0] + " " + heater_data[index_heater][1], heater_FMT)
			last_date_heater = datetime.strptime(heater_data[index_heater-1][0] + " " + heater_data[index_heater-1][1], heater_FMT)
			while next_date_heater < act_date and index_heater + 1 < N_heater:
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
	print "Done with resampling"
	temp.close()

	new_last_index_heater = closest_heater_line

	ind = open('index_file.txt','w')
	ind.write("index_temp:"+str(new_last_index_temp)+"\n")
	ind.write("index_heat:"+str(new_last_index_heater)+"\n")
	ind.close()

if __name__ == '__main__':
    main()