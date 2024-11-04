import requests
import csv
import os

class Weather:
    def __init__(self):
        self.api_key = "727a46ff2be3a94e1626f2303e1ee7008bbaf29554733280ff086e9b2118646b"
        self.base_url = "https://api.meteo-concept.com/api/forecast/daily/0?token="
        self.default_city_name = "toulouse"
        
    def get_weather(self, city_insee):
        url = self.base_url + self.api_key + "&insee=" + city_insee
        response = requests.get(url)
        data = response.json()
        response = {"Ville": data['city']['name'], "Temperature Min": data['forecast']['tmin'], "Temperature Max": data['forecast']['tmax'], "Vent": data['forecast']['wind10m'], "sun_hours": data['forecast']['sun_hours'], "Chance de pluie": data['forecast']['probarain']}
        return response
    
    def display_weather(self, city_insee):
        weather = self.get_weather(city_insee)
        weather_info = f"""
        Ville : {weather['Ville']}
        Température Min : {weather['Temperature Min']}°C
        Température Max : {weather['Temperature Max']}°C
        Vent : {weather['Vent']} km/h
        Nombres d'heures ensoleillé : {weather['sun_hours']} h
        Chance de pluie : {weather['Chance de pluie']} %
        """
        print(weather_info)
        return f"La météo à {weather['Ville']}, Température de : {weather['Temperature Min']}°C à {weather['Temperature Max']}°C. Le vent souffle à {weather['Vent']} km/h. Il y a {weather['sun_hours']} heures d'ensoleillement et une chance de pluie de {weather['Chance de pluie']} %."
    
    def get_city_in_user_input(self, user_input):
        city_name = ""
        csv_file = os.path.join(os.path.dirname(__file__), "data", "cities.csv")
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            city_reader = csv.reader(csvfile)
            cities = {row[3].lower() for row in city_reader if len(row) > 3 and row[3].lower() != "label"}
        
        for word in user_input.lower().split():
            if word in cities:
                city_name = word
                break
        return city_name
    
    def get_insee(self, city_name):
        csv_file = os.path.join(os.path.dirname(__file__), "data", "cities.csv")
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            city_reader = csv.reader(csvfile)
            for row in city_reader:
                if len(row) > 3 and row[3].lower() == city_name:
                    return row[0]
        return None
    
    def user_askMeteo(self, user_input):
        if any(phrase in user_input.lower() for phrase in ['meteo', 'quelle temps fait il', 'temps', 'température', 'temperature', 'météo', 'météo aujourd\'hui']):
            return True
        else:
            return False