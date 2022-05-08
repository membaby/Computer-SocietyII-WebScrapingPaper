import requests
import csv
import time
import datetime

OpenWeatherAPIKey = 'THIS_IS_A_CONFIDENTIAL_API_CODE'
LATITUDE = '31.205753'
LONGITUDE = '29.924526'

def getWeather():
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&&units=metric&appid='+OpenWeatherAPIKey)
    response_json = r.json()
    main = response_json['main']
    data = [main['temp'], main['feels_like'], main['temp_min'], main['temp_max'], main['pressure'], main['humidity']]
    with open('data.csv', 'a+', newline='') as file:
        csv.writer(file).writerow(data)
    message = f'Date: {datetime.datetime.now().strftime("%d %m %Y")} ({response_json["weather"][0]["main"]})\nTemperature: {main["temp"]}\nFeels Like: {main["feels_like"]}\nMin. Temp: {main["temp_min"]}\nMax. Temp: {main["temp_max"]}\nPressure: {main["pressure"]}\n Humidity: {main["humidity"]}'
    requests.get(f'https://api.telegram.org/bot5317602586:THIS_IS_A_CONFIDENTIAL_API_CODE/sendMessage?chat_id=-789596384&text={str(message)}')
    print(data)

while True:
    getWeather()
    time.sleep(86400)

    