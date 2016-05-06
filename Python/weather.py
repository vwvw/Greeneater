import requests,json, datetime
key = 'xxxx' # Wunderground ID for API
url_weather = 'http://api.wunderground.com/api/'+key+'/hourly/q/15217.json'
resp = requests.get(url=url_weather)
weather_data = json.loads(resp.text)
nbr_hours = 10

with open('weather_forecast.txt', 'w') as weather_file:
	for i in range(0, nbr_hours):
		date_json = weather_data['hourly_forecast'][i]['FCTTIME']
		date = datetime.datetime(year=int(date_json['year']), month=int(date_json['mon']), day=int(date_json['mday']),hour=int(date_json['hour']))
		temp = int(weather_data['hourly_forecast'][i]['temp']['metric'])
		weather_file.write(str(date)+" "+str(temp)+"\n")
