import customtkinter as ctk
from PIL import Image
import requests
import time
import datetime
import json
from panels import *

settingsData = json.load(open("settings.json"))

APP_SIZE = settingsData['APP_SIZE']
DEFAULT_CITY = settingsData['DEFAULT_CITY']
DEFAULT_UNIT = settingsData['DEFAULT_UNIT']
SEARCH_BAR_LOCATION = settingsData['SEARCH_BAR_LOCATION']
CITIES_LOCATION = settingsData['CITIES_LOCATION']
TEMP_TYPE = settingsData['TEMP_TYPE']
WIDGETS_PADX = settingsData['WIDGETS_PADX']
WIDGETS_PADY = settingsData['WIDGETS_PADY']
WIDGETS_POSITIONS = settingsData['WIDGETS_POSITIONS']
FONT = settingsData['FONT']
MAIN_TEXT_SIZE = settingsData['MAIN_TEXT_SIZE']
INPUT_FONT_SIZE = settingsData['INPUT_FONT_SIZE']
DETAIL_FONT_SIZE = settingsData['DETAIL_FONT_SIZE']
SMALL_DETAIL_FONT_SIZE = settingsData['SMALL_DETAIL_FONT_SIZE']
BUTTON_CORNER_RADIUS = settingsData['BUTTON_CORNER_RADIUS']
INPUT_CORNER_RADIUS = settingsData['INPUT_CORNER_RADIUS']
SWITCH_FONT_SIZE = settingsData['SWITCH_FONT_SIZE']
GREEN = settingsData['GREEN']
DARK_GREEN = settingsData['DARK_GREEN']
LIGHT_BLUE = settingsData['LIGHT_BLUE']
WHITE = settingsData['WHITE']
BLACK = settingsData['BLACK']
LIGHT_GRAY = settingsData['LIGHT_GRAY']
GRAY = settingsData['GRAY']
DARK_GRAY = settingsData['DARK_GRAY']

class maxWeatherDetails(ctk.CTkFrame):
    def __init__(self, parent, city, metricBoolVar, weatherImage):
        super().__init__(master=parent, fg_color=WHITE, corner_radius=INPUT_CORNER_RADIUS)
        if SEARCH_BAR_LOCATION.lower() == "bottom":
            weatherDetailsRow = 0
        else:
            weatherDetailsRow = 1
        if CITIES_LOCATION.lower() == "left":
            weatherDetailsCol = 1
        else:
            weatherDetailsCol = 0
        self.grid(column=weatherDetailsCol, row=weatherDetailsRow, sticky='nsew', padx=10, pady=10)
        self.city = city
        self.metricBool = metricBoolVar
        self.weatherImage = weatherImage
        
        self.cityTextVar = ctk.StringVar()
        self.mainDetailsVar = ctk.StringVar()
        self.tempDetailsVar = ctk.StringVar()
        self.windDetailsVar = ctk.StringVar()
        self.minMaxDetailsVar = ctk.StringVar()
        self.humidityDetailsVar = ctk.StringVar()
        self.visibilityDetailsVar = ctk.StringVar()
        self.sunDetailsVar = ctk.StringVar()
        self.pressureDetailsVar = ctk.StringVar()
        self.forecastData = {}
        
        self.rowconfigure((0,1,2,3,4), weight=1, uniform='c')
        self.columnconfigure((0,1,2), weight=1, uniform='c')
        
        if WIDGETS_POSITIONS['main']['show']:
            self.mainDetails = mainDetailsPanel(self, self.mainDetailsVar, self.cityTextVar, self.tempDetailsVar, self.weatherImage)
        if WIDGETS_POSITIONS['wind']['show']:
            windDetails = detailsPanel(self, 'wind', self.windDetailsVar)
        if WIDGETS_POSITIONS['minMax']['show']:
            minMaxDetails = detailsPanel(self, 'minMax', self.minMaxDetailsVar)
        if WIDGETS_POSITIONS['humidity']['show']:
            humidityDetails = detailsPanel(self, 'humidity', self.humidityDetailsVar)
        if WIDGETS_POSITIONS['visibility']['show']:
            visibilityDetails = detailsPanel(self, 'visibility', self.visibilityDetailsVar)
        if WIDGETS_POSITIONS['sun']['show']:
            sunDetails = detailsPanel(self, 'sun', self.sunDetailsVar)
        if WIDGETS_POSITIONS['pressure']['show']:
            pressureDetails = detailsPanel(self, 'pressure', self.pressureDetailsVar)
        
        if WIDGETS_POSITIONS['forecast']['show']:
            self.forecastDetails = horizontalForecastPanel(
                self, 
                self.forecastData, 
                self.metricBool, 
                WIDGETS_POSITIONS['forecast']['col'], 
                WIDGETS_POSITIONS['forecast']['row'], 
                WIDGETS_POSITIONS['forecast']['span'], 
                WIDGETS_POSITIONS['forecast']['rowspan'], 
                WHITE
            )
        
        self.getWeatherData(city=self.city.get())
    
    def getWeatherData(self, event=None, city=None):
        if city:
            try:
                if self.metricBool.get():
                    tempSign = "°C"
                    tempUnits = "metric"
                    speedUnits = "km"
                else:
                    tempSign = "°F"
                    tempUnits = "imperial"
                    speedUnits = "mi"
                api = "https://api.openweathermap.org/data/2.5/forecast?units=" + tempUnits + "&q=" + city +"&appid=3473cd8ff0d278ea2f8e67a69c8dd938"
                response = requests.get(api)
                if response.status_code == 200:
                    jsonData = response.json()
                    self.forecastData = {}
                    for key, value in jsonData.items():
                        if key == 'list':
                            for index, dataEntry in enumerate(value):
                                if index == 0:
                                    today = dataEntry['dt_txt'].split(' ')[0]
                                else:
                                    if dataEntry['dt_txt'].split(' ')[0] != today:
                                        if dataEntry['dt_txt'].split(' ')[1] == '12:00:00':
                                            date = dataEntry['dt_txt'].split(' ')[0]
                                            self.forecastData[date] = dataEntry
                    self.forecastDetails.updateData(self.forecastData)
                    api = "https://api.openweathermap.org/data/2.5/weather?units=" + tempUnits + "&q=" + city +"&appid=3473cd8ff0d278ea2f8e67a69c8dd938"
                    todayJsonData = requests.get(api).json()
                    
                    countryName = todayJsonData["sys"]["country"]
                    cityName = todayJsonData["name"]
                    condition = todayJsonData["weather"][0]["main"]
                    description = todayJsonData["weather"][0]["description"]
                    temp = str(int(todayJsonData["main"][TEMP_TYPE])) + tempSign
                    minTemp = str(int(todayJsonData["main"]["temp_min"])) + tempSign
                    maxTemp = str(int(todayJsonData["main"]["temp_max"])) + tempSign
                    humidity = todayJsonData["main"]["humidity"]
                    visibility = todayJsonData["visibility"]
                    windSpeed = todayJsonData["wind"]["speed"]
                    pressure = todayJsonData["main"]["humidity"]
                    try:
                        windGust = todayJsonData["wind"]["gust"]
                    except:
                        windGust = None
                    unformattedSunriseTime = datetime.datetime.utcfromtimestamp(int(todayJsonData['sys']['sunrise']) + int(todayJsonData['timezone']))
                    unformattedSunsetTime = datetime.datetime.utcfromtimestamp(int(todayJsonData['sys']['sunset']) + int(todayJsonData['timezone']))
                    sunrise = unformattedSunriseTime.strftime('%I:%M:%S %p')
                    sunset = unformattedSunsetTime.strftime('%I:%M:%S %p')
                    
                    iconUrl = str(todayJsonData["weather"][0]["icon"])
                    url = "./img/" + iconUrl + "@2x.png"
                    self.weatherImage = Image.open(url)
                    if WIDGETS_POSITIONS['main']['show']:
                        self.mainDetails.imageCanvas.updateImage(self.weatherImage)
        
                    if str(condition).lower() == "clouds" or str(condition).lower() == "" or str(condition).lower() == "thunderstorm":
                        grammarWord = ""
                    elif str(condition).lower() == "clear":
                        grammarWord = " Skies"
                    else:
                        grammarWord = "y Skies"
                    
                    mainDetailsBefore = str(condition) + grammarWord
                    if str(condition).lower() == str(description).split(" ")[0].lower():
                        mainDetails = mainDetailsBefore
                    else:
                        mainDetails = mainDetailsBefore + ", " + str(description) 
                    tempDetails = str(temp)
                    windDetails = str(windSpeed) + str(speedUnits) + " winds"
                    if windGust:
                        windDetails += "\nwith gusts up to " + str(windGust) + str(speedUnits)
                    minMaxDetails = str(minTemp) + " - " + str(maxTemp)
                    humidityDetails = str(humidity) + "%"
                    visibilityDetails = str(visibility/100) + "%"
                    sunDetails = f"{str(sunrise)}\n{str(sunset)}"
                    pressureDetails = str(pressure) + "mb"
                    
                    self.cityTextVar.set(str(cityName) + ", " + str(countryName))
                    self.mainDetailsVar.set(mainDetails)
                    self.tempDetailsVar.set(tempDetails)
                    self.windDetailsVar.set(windDetails)
                    self.minMaxDetailsVar.set(minMaxDetails)
                    self.humidityDetailsVar.set(humidityDetails)
                    self.visibilityDetailsVar.set(visibilityDetails)
                    self.sunDetailsVar.set(sunDetails)
                    self.pressureDetailsVar.set(pressureDetails)
                else:
                    self.clearWeatherDetails("No data found")
            except:
                self.clearWeatherDetails("No city found")
        else:
            self.clearWeatherDetails("No city selected")
        
    def clearWeatherDetails(self, message):
        url = "./img/01n@2x.png"
        self.weatherImage = Image.open(url)
        if WIDGETS_POSITIONS['main']['show']:
            self.mainDetails.imageCanvas.updateImage(self.weatherImage)
        self.cityTextVar.set(message)
        self.mainDetailsVar.set("")
        self.tempDetailsVar.set("")
        self.windDetailsVar.set("")
        self.minMaxDetailsVar.set("")
        self.humidityDetailsVar.set("")
        self.visibilityDetailsVar.set("")
        self.sunDetailsVar.set("")
        self.pressureDetailsVar.set("")
        self.forecastData = {}
        self.forecastDetails.updateData(self.forecastData)
        
class wideWeatherDetails(ctk.CTkFrame):
    def __init__(self, parent, city, metricBoolVar, weatherImage):
        super().__init__(master=parent, fg_color=WHITE, corner_radius=INPUT_CORNER_RADIUS)
        self.grid(column=0, row=0, columnspan=2, rowspan=2, sticky='nsew', padx=10, pady=10)
        self.city = city
        self.metricBool = metricBoolVar
        self.weatherImage = weatherImage
        
        self.cityTextVar = ctk.StringVar()
        self.mainDetailsVar = ctk.StringVar()
        self.tempDetailsVar = ctk.StringVar()
        self.windDetailsVar = ctk.StringVar()
        self.minMaxDetailsVar = ctk.StringVar()
        self.humidityDetailsVar = ctk.StringVar()
        self.visibilityDetailsVar = ctk.StringVar()
        self.sunDetailsVar = ctk.StringVar()
        self.pressureDetailsVar = ctk.StringVar()
        self.forecastData = {}
        
        self.rowconfigure((0,1,2,3,4), weight=1, uniform='c')
        self.columnconfigure((0,1,2), weight=1, uniform='c')
        
        if WIDGETS_POSITIONS['main']['show']:
            self.mainDetails = mainDetailsPanel(self, self.mainDetailsVar, self.cityTextVar, self.tempDetailsVar, self.weatherImage)
        if WIDGETS_POSITIONS['wind']['show']:
            windDetails = detailsPanel(self, 'wind', self.windDetailsVar)
        if WIDGETS_POSITIONS['minMax']['show']:
            minMaxDetails = detailsPanel(self, 'minMax', self.minMaxDetailsVar)
        if WIDGETS_POSITIONS['humidity']['show']:
            humidityDetails = detailsPanel(self, 'humidity', self.humidityDetailsVar)
        if WIDGETS_POSITIONS['visibility']['show']:
            visibilityDetails = detailsPanel(self, 'visibility', self.visibilityDetailsVar)
        if WIDGETS_POSITIONS['sun']['show']:
            sunDetails = detailsPanel(self, 'sun', self.sunDetailsVar)
        if WIDGETS_POSITIONS['pressure']['show']:
            pressureDetails = detailsPanel(self, 'pressure', self.pressureDetailsVar)
        
        if WIDGETS_POSITIONS['forecast']['show']:
            self.forecastDetails = horizontalForecastPanel(
                self, 
                self.forecastData, 
                self.metricBool, 
                WIDGETS_POSITIONS['forecast']['col'], 
                WIDGETS_POSITIONS['forecast']['row'], 
                WIDGETS_POSITIONS['forecast']['span'], 
                WIDGETS_POSITIONS['forecast']['rowspan'], 
                WHITE
            )
        
        self.getWeatherData(city=self.city.get())
    
    def getWeatherData(self, event=None, city=None):
        if city:
            try:
                if self.metricBool.get():
                    tempSign = "°C"
                    tempUnits = "metric"
                    speedUnits = "km"
                else:
                    tempSign = "°F"
                    tempUnits = "imperial"
                    speedUnits = "mi"
                api = "https://api.openweathermap.org/data/2.5/forecast?units=" + tempUnits + "&q=" + city +"&appid=3473cd8ff0d278ea2f8e67a69c8dd938"
                response = requests.get(api)
                if response.status_code == 200:
                    jsonData = response.json()
                    self.forecastData = {}
                    for key, value in jsonData.items():
                        if key == 'list':
                            for index, dataEntry in enumerate(value):
                                if index == 0:
                                    today = dataEntry['dt_txt'].split(' ')[0]
                                else:
                                    if dataEntry['dt_txt'].split(' ')[0] != today:
                                        if dataEntry['dt_txt'].split(' ')[1] == '12:00:00':
                                            date = dataEntry['dt_txt'].split(' ')[0]
                                            self.forecastData[date] = dataEntry
                    self.forecastDetails.updateData(self.forecastData)
                    api = "https://api.openweathermap.org/data/2.5/weather?units=" + tempUnits + "&q=" + city +"&appid=3473cd8ff0d278ea2f8e67a69c8dd938"
                    todayJsonData = requests.get(api).json()
                    
                    countryName = todayJsonData["sys"]["country"]
                    cityName = todayJsonData["name"]
                    condition = todayJsonData["weather"][0]["main"]
                    description = todayJsonData["weather"][0]["description"]
                    temp = str(int(todayJsonData["main"][TEMP_TYPE])) + tempSign
                    minTemp = str(int(todayJsonData["main"]["temp_min"])) + tempSign
                    maxTemp = str(int(todayJsonData["main"]["temp_max"])) + tempSign
                    humidity = todayJsonData["main"]["humidity"]
                    visibility = todayJsonData["visibility"]
                    windSpeed = todayJsonData["wind"]["speed"]
                    pressure = todayJsonData["main"]["humidity"]
                    try:
                        windGust = todayJsonData["wind"]["gust"]
                    except:
                        windGust = None
                    unformattedSunriseTime = datetime.datetime.utcfromtimestamp(int(todayJsonData['sys']['sunrise']) + int(todayJsonData['timezone']))
                    unformattedSunsetTime = datetime.datetime.utcfromtimestamp(int(todayJsonData['sys']['sunset']) + int(todayJsonData['timezone']))
                    sunrise = unformattedSunriseTime.strftime('%I:%M:%S %p')
                    sunset = unformattedSunsetTime.strftime('%I:%M:%S %p')
                    
                    iconUrl = str(todayJsonData["weather"][0]["icon"])
                    url = "./img/" + iconUrl + "@2x.png"
                    self.weatherImage = Image.open(url)
                    if WIDGETS_POSITIONS['main']['show']:
                        self.mainDetails.imageCanvas.updateImage(self.weatherImage)
        
                    if str(condition).lower() == "clouds" or str(condition).lower() == "" or str(condition).lower() == "thunderstorm":
                        grammarWord = ""
                    elif str(condition).lower() == "clear":
                        grammarWord = " Skies"
                    else:
                        grammarWord = "y Skies"
                    
                    mainDetailsBefore = str(condition) + grammarWord
                    if str(condition).lower() == str(description).split(" ")[0].lower():
                        mainDetails = mainDetailsBefore
                    else:
                        mainDetails = mainDetailsBefore + ", " + str(description) 
                    tempDetails = str(temp)
                    windDetails = str(windSpeed) + str(speedUnits) + " winds"
                    if windGust:
                        windDetails += "\nwith gusts up to " + str(windGust) + str(speedUnits)
                    minMaxDetails = str(minTemp) + " - " + str(maxTemp)
                    humidityDetails = str(humidity) + "%"
                    visibilityDetails = str(visibility/100) + "%"
                    sunDetails = f"{str(sunrise)}\n{str(sunset)}"
                    pressureDetails = str(pressure) + "mb"
                    
                    self.cityTextVar.set(str(cityName) + ", " + str(countryName))
                    self.mainDetailsVar.set(mainDetails)
                    self.tempDetailsVar.set(tempDetails)
                    self.windDetailsVar.set(windDetails)
                    self.minMaxDetailsVar.set(minMaxDetails)
                    self.humidityDetailsVar.set(humidityDetails)
                    self.visibilityDetailsVar.set(visibilityDetails)
                    self.sunDetailsVar.set(sunDetails)
                    self.pressureDetailsVar.set(pressureDetails)
                else:
                    url = "./img/01n@2x.png"
                    self.weatherImage = Image.open(url)
                    if WIDGETS_POSITIONS['main']['show']:
                        self.mainDetails.imageCanvas.updateImage(self.weatherImage)
                    self.clearWeatherDetails("No data found")
            except:
                url = "./img/01n@2x.png"
                self.weatherImage = Image.open(url)
                if WIDGETS_POSITIONS['main']['show']:
                    self.mainDetails.imageCanvas.updateImage(self.weatherImage)
                self.clearWeatherDetails("No city found")
        else:
            url = "./img/01n@2x.png"
            self.weatherImage = Image.open(url)
            if WIDGETS_POSITIONS['main']['show']:
                self.mainDetails.imageCanvas.updateImage(self.weatherImage)
            self.clearWeatherDetails("No city selected")
        
    def clearWeatherDetails(self, message):
        self.cityTextVar.set(message)
        self.mainDetailsVar.set("")
        self.tempDetailsVar.set("")
        self.windDetailsVar.set("")
        self.minMaxDetailsVar.set("")
        self.humidityDetailsVar.set("")
        self.visibilityDetailsVar.set("")
        self.sunDetailsVar.set("")
        self.pressureDetailsVar.set("")
        self.forecastData = {}
        self.forecastDetails.updateData(self.forecastData)
        
class smallWeatherDetails(ctk.CTkFrame):
    def __init__(self, parent, city, metricBoolVar, weatherImage, row, rowspan):
        super().__init__(master=parent, fg_color=WHITE, corner_radius=INPUT_CORNER_RADIUS)
        self.grid(column=0, row=row, columnspan=2, rowspan=rowspan, sticky='nsew', padx=10, pady=10)
        self.city = city
        self.metricBool = metricBoolVar
        self.weatherImage = weatherImage
        
        self.cityTextVar = ctk.StringVar()
        self.mainDetailsVar = ctk.StringVar()
        self.tempDetailsVar = ctk.StringVar()
        
        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=1, uniform='b')
        
        self.mainDetails = mainDetailsPanel(self, self.mainDetailsVar, self.cityTextVar, self.tempDetailsVar, self.weatherImage, 0, 0, 1, 1, 'transparent')        
        self.getWeatherData(city=self.city.get())
    
    def getWeatherData(self, event=None, city=None):
        if city:
            try:
                if self.metricBool.get():
                    tempSign = "°C"
                    tempUnits = "metric"
                else:
                    tempSign = "°F"
                    tempUnits = "imperial"
                api = "https://api.openweathermap.org/data/2.5/weather?units=" + tempUnits + "&q=" + city +"&appid=3473cd8ff0d278ea2f8e67a69c8dd938"
                todayJsonData = requests.get(api).json()
                
                countryName = todayJsonData["sys"]["country"]
                cityName = todayJsonData["name"]
                condition = todayJsonData["weather"][0]["main"]
                description = todayJsonData["weather"][0]["description"]
                temp = str(int(todayJsonData["main"][TEMP_TYPE])) + tempSign
                
                iconUrl = str(todayJsonData["weather"][0]["icon"])
                url = "./img/" + iconUrl + "@2x.png"
                self.weatherImage = Image.open(url)
                self.mainDetails.imageCanvas.updateImage(self.weatherImage)
    
                if str(condition).lower() == "clouds" or str(condition).lower() == "" or str(condition).lower() == "thunderstorm":
                    grammarWord = ""
                elif str(condition).lower() == "clear":
                    grammarWord = " Skies"
                else:
                    grammarWord = "y Skies"
                
                mainDetailsBefore = str(condition) + grammarWord
                if str(condition).lower() == str(description).split(" ")[0].lower():
                    mainDetails = mainDetailsBefore
                else:
                    mainDetails = mainDetailsBefore + ", " + str(description) 
                tempDetails = str(temp)
                
                self.cityTextVar.set(str(cityName) + ", " + str(countryName))
                self.mainDetailsVar.set(mainDetails)
                self.tempDetailsVar.set(tempDetails)
            except:
                url = "./img/01n@2x.png"
                self.weatherImage = Image.open(url)
                self.mainDetails.imageCanvas.updateImage(self.weatherImage)
                self.clearWeatherDetails("No city found")
        else:
            url = "./img/01n@2x.png"
            self.weatherImage = Image.open(url)
            self.mainDetails.imageCanvas.updateImage(self.weatherImage)
            self.clearWeatherDetails("No city selected")
        
    def clearWeatherDetails(self, message):
        self.cityTextVar.set(message)
        self.mainDetailsVar.set("")
        self.tempDetailsVar.set("")