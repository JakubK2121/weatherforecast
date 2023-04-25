import requests
import json
import datetime
from key import API_KEY

API_URL = "https://api.weatherapi.com/v1/forecast.json"


def weather_forecast(select, city, date, forecasts):
    for forecast in forecasts:
        outcome = forecast["day"][select]
        print(f"The {fmessage} in {city} will be {outcome}{s} on {date}.")


def chosen(var, x, result):
    if var == str(x):
        select = result
        return select


while True:
    welcome = input(
        "Welcome!\nChoose which weather parameter you would like to check today:\n1. Temperature\n2. Wind\n3. Precip\n4. Humidity\n5. Chance of rain\n")
    if welcome == "1":
        temp = input(
            "Choose which temperature parameter you would like to check?\n1. Maximum temperature\n2. Minimum temperature\n3. Average temperature\n")
        if temp == "1":
            select = chosen(temp, 1, "maxtemp_c")
            fmessage = "maximum temperature"
        if temp == "2":
            select = chosen(temp, 2, "mintemp_c")
            fmessage = "minimum temperature"
        if temp == "3":
            select = chosen(temp, 3, "avgtemp_c")
            fmessage = "average temperature"
        s = "°C"
        break
    elif welcome == "2":
        wind = input("Choose which wind parameter you would like to check?\n1. Maximum wind strength\n")
        select = chosen(wind, 1, "maxwind_kph")
        fmessage = "maximum wind strength"
        s = "kph"
        break
    elif welcome == "3":
        precip = input("Choose which precip parameter you would like to check?\n1. Total precipitation\n")
        select = chosen(precip, 1, "totalprecip_mm")
        fmessage = "total precipitation"
        s = "mm"
        break
    elif welcome == "4":
        humidity = input("Choose which humidity parameter you would like to check?\n1. Average Humidity \n")
        select = chosen(humidity, 1, "avghumidity")
        fmessage = "average humidity"
        s = "%"
        break
    elif welcome == "5":

        cor = input("Check the chance of rainfall.\n1. Chance of rain\n")
        select = chosen(cor, 1, "daily_chance_of_rain")
        fmessage = "chance of rain"
        s = "%"
        break
    else:
        print("Invalid value! Try again")

date = input("Enter date in format YYYY-MM-DD: ")
city = input("Enter city: ")
days = 3

current_date = datetime.datetime.now().date()
future_date = current_date + datetime.timedelta(days)

params = {
    "key": API_KEY,
    "q": city,
    "date": date,
}

response = requests.get(API_URL, params=params)
weather_data = response.json()
json_string = json.dumps(weather_data, indent=4)

try:
    user_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if user_date >= current_date and user_date <= future_date:
        if response.status_code == 200:
            weather_data = response.json()
            if "forecast" in weather_data:
                forecasts = weather_data["forecast"]["forecastday"]
                weather_forecast(select, city, date, forecasts)

            else:
                print("No weather forecasts in the API response")
        elif "No matching location found." in response.json()["error"]["message"]:
            print("No matching location found.")
        else:
            print(f"Error when sending request to API {response.status_code} check if your API key is correct")
    else:
        print(f"Invalid date. Date should not be smaller than current date or bigger than current date + {days} days")
except ValueError:
    print("Invalid date format. Please enter date in format YYYY-MM-DD.")