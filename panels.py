import customtkinter as ctk
from PIL import Image
import datetime, calendar
import requests
import json
from imageWidgets import *

settingsData = json.load(open("settings.json"))

APP_SIZE = settingsData['APP_SIZE']
DEFAULT_CITY = settingsData['DEFAULT_CITY']
DEFAULT_UNIT = settingsData['DEFAULT_UNIT']
SEARCH_BAR_LOCATION = settingsData['SEARCH_BAR_LOCATION']
CITIES_LOCATION = settingsData['CITIES_LOCATION']
TEMP_TYPE = settingsData['TEMP_TYPE']
QUICK_CITIES = settingsData['QUICK_CITIES']
WIDGETS_PADX = settingsData['WIDGETS_PADX']
WIDGETS_PADY = settingsData['WIDGETS_PADY']
WIDGETS_POSITIONS = settingsData['WIDGETS_POSITIONS']
FONT = settingsData['FONT']
MAIN_TEXT_SIZE = settingsData['MAIN_TEXT_SIZE']
MEDIUM_TEXT_SIZE = settingsData['MEDIUM_TEXT_SIZE']
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

def getTimeInfo():
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    weekday = list(calendar.day_name)[datetime.datetime.today().weekday()]
    
    match day % 10:
        case 1: suffix = 'st'
        case 2: suffix = 'nd'
        case 3: suffix = 'rd'
        case _: suffix = 'th'
        
    return day, weekday, suffix, month

def getWeatherInfo(city, metricBool):
    if metricBool:
        tempUnits = 'metric'
    else:
        tempUnits = 'imperial'    
    api = "https://api.openweathermap.org/data/2.5/weather?units=" + tempUnits + "&q=" + city +"&appid=3473cd8ff0d278ea2f8e67a69c8dd938"
    return requests.get(api).json()

def updateJsonFile(filePath, keyToUpdate, newValue):
    with open(filePath, 'r') as file:
        data = json.load(file)
    data[keyToUpdate] = newValue
    with open(filePath, 'w') as file:
        json.dump(data, file, indent=4)

class detailsPanel(ctk.CTkFrame):
    def __init__(self, parent, detail, detailsVar):
        self.detailsVar = detailsVar
        super().__init__(
            master=parent,
            fg_color=LIGHT_BLUE,
            corner_radius=INPUT_CORNER_RADIUS
        )
        self.grid(
            row=WIDGETS_POSITIONS[detail]['row'], 
            column=WIDGETS_POSITIONS[detail]['col'], 
            sticky='nsew', 
            columnspan=WIDGETS_POSITIONS[detail]['span'], 
            rowspan=WIDGETS_POSITIONS[detail]['rowspan'],
            padx=WIDGETS_PADX, 
            pady=WIDGETS_PADY
        )
        
        self.rowconfigure((0,1,3), weight=1, uniform='d')
        self.rowconfigure(2, weight=4, uniform='d')
        self.columnconfigure(0, weight=1, uniform='d')
        
        ctk.CTkLabel(
            master=self, 
            font=ctk.CTkFont(family=FONT, size=SMALL_DETAIL_FONT_SIZE), 
            fg_color='transparent', 
            text=WIDGETS_POSITIONS[detail]['text'], 
            text_color=BLACK
        ).grid(column=0, row=1)
        
        ctk.CTkLabel(
            master=self, 
            font=ctk.CTkFont(family=FONT, size=DETAIL_FONT_SIZE), 
            fg_color='transparent', 
            text_color=BLACK, 
            textvariable=self.detailsVar
        ).grid(column=0, row=2)
        
class mainDetailsPanel(ctk.CTkFrame):
    def __init__(self, parent, detailsVar, cityVar, tempVar, image, row=WIDGETS_POSITIONS['main']['row'], col=WIDGETS_POSITIONS['main']['col'], span=WIDGETS_POSITIONS['main']['span'], rowspan=WIDGETS_POSITIONS['main']['rowspan'], color=LIGHT_BLUE):
        self.detailsVar = detailsVar
        self.cityVar = cityVar
        self.tempVar = tempVar
        self.image = image
        super().__init__(
            master=parent,
            fg_color=color,
            corner_radius=INPUT_CORNER_RADIUS
        )
        self.grid(
            row=row, 
            column=col, 
            sticky='nsew', 
            columnspan=span, 
            rowspan=rowspan,
            padx=WIDGETS_PADX, 
            pady=WIDGETS_PADY
        )
        
        self.rowconfigure((0,1), weight=1, uniform='e')
        self.rowconfigure(2, weight=4, uniform='e')
        self.rowconfigure(3, weight=2, uniform='e')
        self.columnconfigure(0, weight=1, uniform='e')
        
        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        ctk.CTkLabel(
            master=self, 
            textvariable=self.cityVar, 
            font=font,
            text_color=BLACK
        ).grid(column=0, row=0, sticky='nsew', padx=10, pady=10)
        
        day, weekday, suffix, month = getTimeInfo()
        ctk.CTkLabel(
            self, 
            text=f'{weekday[:3]}, {calendar.month_name[month]} {day}{suffix}',
            font=font,
            text_color=BLACK
        ).grid(column=0, row=1, sticky='nsew', padx=10, pady=10)
        
        ctk.CTkLabel(
            self, 
            textvariable=self.tempVar,
            font=ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE),
            text_color=BLACK
        ).grid(column=0, row=3, sticky='nsew', padx=10, pady=10)
        
        ctk.CTkLabel(
            self, 
            textvariable=self.detailsVar,
            font=font,
            text_color=BLACK
        ).grid(column=0, row=4, sticky='nsew', padx=10, pady=10)
        
        if color == 'transparent':
            imageColor = WHITE
        else:
            imageColor = color
        
        self.imageCanvas = staticImage(self, self.image, 0, 2, imageColor, WIDGETS_PADX, WIDGETS_PADY)
        
class horizontalForecastPanel(ctk.CTkFrame):
    def __init__(self, parent, data, metricBool, col, row, span, rowspan, dividerColor):
        super().__init__(master=parent, fg_color=LIGHT_BLUE)
        self.grid(column=col, row=row, columnspan=span, rowspan=rowspan, sticky='nsew', padx=6, pady=6)
        self.metricBool = metricBool
        self.dividerColor = dividerColor
        self.frames = []
        self.dividers = []
        
        for index, info in enumerate(data.items()):
            frame = ctk.CTkFrame(self, fg_color='transparent')
            year, month, day = info[0].split('-')
            weekday = list(calendar.day_name)[datetime.date(int(year), int(month), int(day)).weekday()][:3]
            
            frame.rowconfigure(0, weight=5, uniform='d')
            frame.rowconfigure(1, weight=2, uniform='d')
            frame.rowconfigure(2, weight=1, uniform='d')
            frame.columnconfigure(0, weight=1, uniform='d')
            
            url = f'./img/01d@2x.png'
            image = Image.open(url)
            self.imageCanvas = staticImage(frame, image, 0, 0, LIGHT_BLUE, WIDGETS_PADX, WIDGETS_PADY)
            ctk.CTkLabel(frame, text=f'{info[1]["temp"]}', text_color='#444', font=('Calibri', 22)).grid(column=0, row=1, sticky='n')
            ctk.CTkLabel(frame, text=weekday, text_color='#444').grid(column=0, row=2)
            frame.pack(side='left', expand=True, fill='both', padx=5, pady=5)
            self.frames.append(frame)
            
            if index < (len(data) - 1):
                divider = ctk.CTkFrame(self, fg_color=self.dividerColor, width=2)
                divider.pack(side='left', fill='both')
                self.dividers.append(divider)
                
    def updateData(self, data):
        for frame in self.frames: frame.pack_forget()
        for divider in self.dividers: divider.pack_forget()
        for index, info in enumerate(data.items()):
            frame = ctk.CTkFrame(self, fg_color='transparent')
            year, month, day = info[0].split('-')
            weekday = list(calendar.day_name)[datetime.date(int(year), int(month), int(day)).weekday()][:3]
            
            frame.rowconfigure(0, weight=5, uniform='d')
            frame.rowconfigure(1, weight=2, uniform='d')
            frame.rowconfigure(2, weight=1, uniform='d')
            frame.columnconfigure(0, weight=1, uniform='d')
            
            if self.metricBool.get():
                unitSign = '°C'
            else:
                unitSign = '°F'
            
            url = f'./img/{info[1]["weather"][0]["icon"]}@2x.png'
            image = Image.open(url)
            self.imageCanvas = staticImage(frame, image, 0, 0, LIGHT_BLUE, WIDGETS_PADX, WIDGETS_PADY)                
            ctk.CTkLabel(frame, text=f'{int(info[1]["main"][TEMP_TYPE])}{unitSign}', text_color=BLACK, font=ctk.CTkFont(family=FONT, size=DETAIL_FONT_SIZE)).grid(column=0, row=1, sticky='n')
            ctk.CTkLabel(frame, text=weekday, text_color=BLACK, font=ctk.CTkFont(family=FONT, size=SMALL_DETAIL_FONT_SIZE)).grid(column=0, row=2)
            frame.pack(side='left', expand=True, fill='both', padx=5, pady=5)
            self.frames.append(frame)
            
            if index < (len(data) - 1):
                divider = ctk.CTkFrame(self, fg_color=self.dividerColor, width=2)
                divider.pack(side='left', fill='both')
                self.dividers.append(divider)

class citiesPanel(ctk.CTkFrame):
    def __init__(self, parent, weatherDetails, metricBool):
        super().__init__(master=parent, fg_color=WHITE, corner_radius=INPUT_CORNER_RADIUS)
        if CITIES_LOCATION.lower() == "left":
            citiesPanelCol = 0
        else:
            citiesPanelCol = 1
        self.grid(column=citiesPanelCol, row=0, rowspan=2, sticky='nsew', padx=10, pady=10)
        
        self.rowconfigure(0, weight=1, uniform='f')
        self.rowconfigure(1, weight=12, uniform='f')
        self.rowconfigure(2, weight=3, uniform='f')
        self.columnconfigure(0, weight=1, uniform='f')
        
        self.citiesView = citiesView(self, weatherDetails, metricBool)
        self.addBar = addBar(self)
        
class citiesView(ctk.CTkScrollableFrame):
    def __init__(self, parent, parentParent, metricBool):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(column=0, row=1, sticky='nsew')
        self.parentParent = parentParent
        self.metricBool = metricBool
        self.cityFrames = {}
        
        for city in QUICK_CITIES:
            self.addCityFrame(city)
            
    def updateCityFrames(self):
        for cityFrame in self.cityFrames: self.cityFrames[cityFrame].update()
        
        for city in QUICK_CITIES:
            self.addCityFrame(city)
            
    def addCityFrame(self, city):
        jsonData = getWeatherInfo(city, self.metricBool.get())
        cityFrame(self, city, jsonData, self.metricBool, self.cityFrames, self.parentParent)
        
    def removeCityFrame(self, city):
        data = json.load(open('settings.json'))
        newList = data['QUICK_CITIES']
        newList.remove(city)
        updateJsonFile('settings.json', 'QUICK_CITIES', newList)
        self.cityFrames[city].pack_forget()
        self.cityFrames.pop(city)
        
class cityFrame(ctk.CTkFrame):
    def __init__(self, parent, city, jsonData, metricBool, cityFrames, parentParent):
        super().__init__(master=parent, fg_color=LIGHT_BLUE, corner_radius=INPUT_CORNER_RADIUS)
        self.city = city
        self.cityFrames = cityFrames
        self.metricBool = metricBool
        self.parentParent = parentParent
        
        if self.metricBool.get():
            tempUnits = '°C'
        else:
            tempUnits = '°F'
        self.metricBool.trace('w', self.update)
        
        self.rowconfigure((0,1), weight=1, uniform='g')
        self.columnconfigure((0,1), weight=1, uniform='g')
        
        self.cityLabel = ctk.CTkLabel(
            self, 
            text=f'{jsonData["name"]}, {jsonData["sys"]["country"]}', 
            font=ctk.CTkFont(family=FONT, size=DETAIL_FONT_SIZE), 
            text_color=BLACK
        )
        self.cityLabel.grid(column=0, row=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        self.cityLabel.bind('<Button>', lambda event, city=self.city: self.parentParent.getWeatherData(event=event, city=city))
        
        self.weatherLabel = ctk.CTkLabel(
            self, 
            text=f'{int(jsonData["main"][TEMP_TYPE])}{tempUnits}', 
            font=ctk.CTkFont(family=FONT, size=MEDIUM_TEXT_SIZE), 
            text_color=BLACK
        )
        self.weatherLabel.grid(column=0, row=1, sticky='nsew', padx=5, pady=5)
        
        url = f'./img/{jsonData["weather"][0]["icon"]}@2x.png'
        image = Image.open(url)
        self.imageCanvas = staticImage(self, image, 1, 1, LIGHT_BLUE, 5, 5) 
        
        self.removeButton = ctk.CTkButton(
            self,
            text='x',
            fg_color='transparent',
            width=10,
            height=10,
            hover_color=LIGHT_BLUE,
            command=lambda city=self.city: parent.removeCityFrame(city),
            font=ctk.CTkFont(family=FONT, size=SMALL_DETAIL_FONT_SIZE),
            text_color=BLACK
        )
        self.removeButton.place(relx=0.9, rely=0.1, anchor='center')
        self.removeButton.bind('<Enter>', self.hoverHandler)
        self.removeButton.bind('<Leave>', self.resetRemoveButton)
        
        self.pack(fill='both', expand=True, padx=WIDGETS_PADX, pady=WIDGETS_PADY)
        self.cityFrames[self.city] = self
        
    def update(self, *args):
        if self.metricBool.get():
            tempUnits = '°C'
        else:
            tempUnits = '°F'      
        jsonData = getWeatherInfo(self.city, self.metricBool.get())
        self.weatherLabel.configure(text=f'{int(jsonData["main"][TEMP_TYPE])}{tempUnits}')
        
    def hoverHandler(self, event):
        self.removeButton.configure(text_color='red')
        
    def resetRemoveButton(self, event):
        self.removeButton.configure(text_color=BLACK)
        
class addBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(column=0, row=2, sticky='nsew', padx=WIDGETS_PADX, pady=WIDGETS_PADY)
        self.parent = parent
        
        self.rowconfigure((0,1), weight=1, uniform='h')
        self.columnconfigure(0, weight=1, uniform='h')
        
        font = ctk.CTkFont(family=FONT, size=DETAIL_FONT_SIZE)
        self.inputBox = ctk.CTkEntry(master=self, fg_color=WHITE, font=font, text_color=BLACK, placeholder_text='Your City', placeholder_text_color=DARK_GRAY, corner_radius=INPUT_CORNER_RADIUS, border_color=GRAY, border_width=4)
        self.inputBox.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)
        
        self.addButton = ctk.CTkButton(self, command=self.addQuickCity, text='Add', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        self.addButton.grid(column=0, row=1, sticky='nsew', padx=5, pady=5)
        
    def addQuickCity(self):
        data = json.load(open('settings.json'))
        newList = data['QUICK_CITIES']
        newList.append(self.inputBox.get())
        updateJsonFile('settings.json', 'QUICK_CITIES', newList)
        try:
            self.parent.citiesView.addCityFrame(self.inputBox.get())
            self.addButton.configure(text_color='green', text='Added')
            self.after(3000, self.resetAddButton)
        except:
            data = json.load(open('settings.json'))
            newList = data['QUICK_CITIES']
            newList.remove(self.inputBox.get())
            updateJsonFile('settings.json', 'QUICK_CITIES', newList)
            self.addButton.configure(text_color='red', text='No city found')
            self.after(3000, self.resetAddButton)
        self.inputBox.delete(0, len(self.inputBox.get()))
    
    def resetAddButton(self):
        self.addButton.configure(text_color=BLACK, text='Add')