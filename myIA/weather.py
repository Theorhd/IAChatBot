import requests
import csv

class Weather:
    def __init__(self):
        self.api_key = "API_KEY"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.default_city_name = "Toulouse"
        
    def get_weather(self, city_name):
        if city_name == "":
            city_name = self.default_city_name
        complete_url = self.base_url + "appid=" + self.api_key + "&q=" + city_name
        response = requests.get(complete_url)
        return response.json()
    
    def get_city_in_user_input(self, user_input):
        city_name = ""
        with open('data/cities.csv', newline='', encoding='utf-8') as csvfile:
            city_reader = csv.reader(csvfile)
            cities = {row[3].lower() for row in city_reader if row[3] != "label"}
        
        for word in user_input.lower().split():
            if word in cities:
                city_name = word
                break
        return city_name
