import customtkinter as ctk
from PIL import Image
from weatherDetails import *
from panels import *
import json
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

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
TITLE_HEX_COLOR = 0x00ABBF50

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = GREEN)
        self.title('')
        self.iconbitmap('empty.ico')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.minsize(APP_SIZE[0], APP_SIZE[1])
        self.changeTitleBarColor()
        self.after(0, lambda:self.state('zoomed'))
        
        if SEARCH_BAR_LOCATION.lower() == "bottom":
            rowZeroWeight = 5
            rowOneWeight = 1
        else:
            rowZeroWeight = 1
            rowOneWeight = 5
        if CITIES_LOCATION.lower() == "left":
            colZeroWeight = 1
            colOneWeight = 4
        else:
            colZeroWeight = 4
            colOneWeight = 1
        
        self.columnconfigure(0, weight=colZeroWeight, uniform='a')
        self.columnconfigure(1, weight=colOneWeight, uniform='a')
        self.rowconfigure(0, weight=rowZeroWeight, uniform='a')
        self.rowconfigure(1, weight=rowOneWeight, uniform='a')
        
        if DEFAULT_UNIT == "metric":
            defaultMetricBoolVar = True
        else:
            defaultMetricBoolVar = False
        self.metricBoolVar = ctk.BooleanVar(value=defaultMetricBoolVar)
        self.cityVar = ctk.StringVar()
        
        self.heightBreak = 800
        self.widthBreak = 1000
        self.fullHeightBool = ctk.BooleanVar(value=False)
        self.fullWidthBool = ctk.BooleanVar(value=False)
        
        self.fullHeightBool.trace('w', self.changeSize)
        self.fullWidthBool.trace('w', self.changeSize)
        
        self.setDefaultCity()
        
        self.cityVar.trace('w', self.updateCity)
        self.metricBoolVar.trace('w', self.changeUnits)
        
        self.searchBar = searchBar(self, self.cityVar, 1)
        self.weatherDetails = maxWeatherDetails(self, self.cityVar, self.metricBoolVar, Image.open("./img/01d@2x.png"))
        self.citiesPanel = citiesPanel(self, self.weatherDetails, self.metricBoolVar)
        unitSwitcher(self.citiesPanel, self.metricBoolVar)
        
        self.bind('<Return>', self.updateCityVar)
        self.bind('<Configure>', self.checkSize)
        
        self.mainloop()
    
    def changeTitleBarColor(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass
    
    def setDefaultCity(self):
        self.cityVar.set(DEFAULT_CITY)
    
    def updateCity(self, *args):
        self.weatherDetails.getWeatherData(city=self.cityVar.get())
        
    def updateCityVar(self, *args):
        self.cityVar.set(self.searchBar.inputBox.get())
        self.searchBar.inputBox.delete(0, len(self.searchBar.inputBox.get()))
        
    def changeUnits(self, *args):
        self.weatherDetails.getWeatherData(city=self.cityVar.get())
    
    def checkSize(self, event):
        if event.widget == self:
            if self.fullWidthBool.get():
                if event.width < self.widthBreak:
                    self.fullWidthBool.set(False)
            else:
                if event.width > self.widthBreak:
                    self.fullWidthBool.set(True)
            
            if self.fullHeightBool.get():
                if event.height < self.heightBreak:
                    self.fullHeightBool.set(False)
            else:
                if event.height > self.heightBreak:
                    self.fullHeightBool.set(True)
                    
    def changeSize(self, *args):
        self.searchBar.grid_forget()
        self.weatherDetails.grid_forget()
        self.citiesPanel.grid_forget()
        
        if self.fullWidthBool.get() and self.fullHeightBool.get():
            self.searchBar = searchBar(self, self.cityVar, 1)
            self.weatherDetails = maxWeatherDetails(self, self.cityVar, self.metricBoolVar, Image.open("./img/01d@2x.png"))
            self.citiesPanel = citiesPanel(self, self.weatherDetails, self.metricBoolVar)
            unitSwitcher(self.citiesPanel, self.metricBoolVar)
            
        if self.fullWidthBool.get() and not self.fullHeightBool.get():
            self.weatherDetails = wideWeatherDetails(self, self.cityVar, self.metricBoolVar, Image.open("./img/01d@2x.png"))
            unitSwitcher(self.weatherDetails, self.metricBoolVar, wide=True)
            
        if not self.fullWidthBool.get() and self.fullHeightBool.get():
            if SEARCH_BAR_LOCATION.lower() == 'bottom':
                row = 0
            else:
                row = 1
            self.searchBar = searchBar(self, self.cityVar, 2, 0)
            self.weatherDetails = smallWeatherDetails(self, self.cityVar, self.metricBoolVar, Image.open("./img/01d@2x.png"), row, 1)
            unitSwitcher(self.weatherDetails, self.metricBoolVar, tall=True)
        
        if not self.fullWidthBool.get() and not self.fullHeightBool.get():
            self.weatherDetails = smallWeatherDetails(self, self.cityVar, self.metricBoolVar, Image.open("./img/01d@2x.png"), 0, 2)
            unitSwitcher(self.weatherDetails, self.metricBoolVar, tall=True)
        
class searchBar(ctk.CTkFrame):
    def __init__(self, parent, city, span, col=None):
        super().__init__(master=parent, fg_color=WHITE, corner_radius=INPUT_CORNER_RADIUS)
        if SEARCH_BAR_LOCATION.lower() == "bottom":
            searchBarRow = 1
        else:
            searchBarRow = 0
        if col is None:
            if CITIES_LOCATION.lower() == "left":
                searchBarCol = 1
            else:
                searchBarCol = 0
        else:
            searchBarCol = col
        self.grid(column=searchBarCol, row=searchBarRow, columnspan=span, sticky='nsew', padx=10, pady=10)
        self.city = city
        
        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=3, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        
        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        
        self.inputBox = ctk.CTkEntry(master=self, fg_color=WHITE, font=font, text_color=BLACK, placeholder_text='Your City', placeholder_text_color=DARK_GRAY, corner_radius=INPUT_CORNER_RADIUS, border_color=GRAY, border_width=4)
        self.inputBox.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)
        
        searchButton = ctk.CTkButton(self, command=self.updateCityVar, text='Search', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        searchButton.grid(row=0, column=1, sticky='nsew', padx=8, pady=5)
    
    def updateCityVar(self, *args):
        self.city.set(self.inputBox.get())
        self.inputBox.delete(0, len(self.inputBox.get()))

class unitSwitcher(ctk.CTkFrame):
    def __init__(self, parent, metricBoolVar, wide=False, tall=False):
        backColor = WHITE
        if wide:
            backColor = LIGHT_BLUE
        super().__init__(master=parent, fg_color=backColor)
        foreColor = LIGHT_GRAY
        if wide:
            self.place(relx=0.5, rely=0.5, anchor='center')
            foreColor = DARK_GREEN
        elif tall:
            self.place(relx=0.1, rely=0.05, anchor='center')
        else:
            self.place(relx=0.5, rely=0.03, anchor='center')
        self.metricBool = metricBoolVar
        
        font = ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE)
        self.unitSwitchButton = ctk.CTkSegmentedButton(
            self, 
            command=self.changeUnits, 
            values=['°C', '°F'], 
            font=font,
            text_color=DARK_GREEN,
            fg_color=foreColor,
            selected_color=LIGHT_BLUE,
            selected_hover_color=GREEN,
            unselected_color=LIGHT_GRAY,
            unselected_hover_color=GRAY
        )
        self.unitSwitchButton.pack(fill='both', expand=True)
        if self.metricBool.get():
            self.unitSwitchButton.set('°C')
        else:
            self.unitSwitchButton.set('°F')
        
    def changeUnits(self, value):
        self.metricBool.set(not self.metricBool.get())
        
        if self.metricBool.get():
            self.unitSwitchButton.set('°C')
        else:
            self.unitSwitchButton.set('°F')

if __name__ == '__main__':   
    App()