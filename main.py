from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
import requests
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineAvatarListItem
from kivy.lang import Builder
from bs4 import BeautifulSoup
from kivy.clock import Clock

Window.size = (350, 600)
KV = """
<Item>

    ImageLeftWidget:
        source: root.source

"""


class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()


class WeatherApp(MDApp):
    dialog = None    
    
    def showRetry(self, dt):
         print("now")
         self.dialog = MDDialog(text="Oops! Something seems to have gone wrong, getting default city, please enter your city below!",radius=[20, 7, 20, 7],buttons=[ MDFlatButton(text="Cancel", on_release=self.close_dialog)])
         self.dialog.open()


    def build(self):
        # self.current_cityv2()
        try:
            current_city = self.current_city()
            self.get_weather(current_city)
            return Builder.load_string(KV)
        except:             
             Clock.schedule_once(self.showRetry, 3)

    def get_weather(self, city):
        # try catch here for openweather error
        result = self.callapi(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d29300a88f0ef96ff3588b6c3e5ec09d"
        )

        if result["cod"] == "404":
            print("city not found")
            self.show_city_not_found()
        else:
            temperature = round(result["main"]["temp"] - 273.15)
            humidity = result["main"]["humidity"]
            weather = result["weather"][0]["main"]
            weather_descrpition = result["weather"][0]["description"]
            weather_id = result["weather"][0]["id"]
            wind_speed = result["wind"]["speed"] * 3.6
            location = result["name"] + ", " + result["sys"]["country"]

            self.root.ids.location.text = location
            self.root.ids.temperature.text = str(temperature) + "°"
            self.root.ids.weather.text = weather_descrpition.title()
            self.root.ids.wind_speed.text = str(round(wind_speed)) + "Km/H"
            self.root.ids.wind.text = self.beaufort(wind_speed)
            self.root.ids.humidity_level.text = str(humidity) + "%"
            self.setimage(int(weather_id))

    def run_searchplaces(self):
        # print(self.root.ids)
        self.get_weather(self.root.ids.new_city.text)

    def beaufort(self, temp):
        if temp >= 118:
            return "hurricane"
        elif temp > 103:
            return "violent storm"
        elif temp > 89:
            return "storm"
        elif temp > 75:
            return "strong gale"
        elif temp > 62:
            return "gale"
        elif temp > 50:
            return "High wind"
        elif temp > 39:
            return "strong breeze"
        elif temp > 29:
            return "Fresh breeze"
        elif temp > 20:
            return "Moderate breeze"
        elif temp > 12:
            return "Gentle breeze"
        elif temp > 6:
            return "Light breeze"
        elif temp > 2:
            return "light air"
        else:
            return "calm"

    def setimage(self, ides):
        if ides > 800:
            self.root.ids.imagew.source = "assets/cloudy.png"

        elif ides == 800:
            self.root.ids.imagew.source = "assets/sun2.png"
        elif ides >= 700:
            self.root.ids.imagew.source = "assets/dust.png"
        elif ides >= 600:
            self.root.ids.imagew.source = "assets/snow.png"
        elif ides >= 500:
            self.root.ids.imagew.source = "assets/rain.png"
        elif ides >= 300:
            self.root.ids.imagew.source = "assets/drizzle.png"
        elif ides >= 200:
            self.root.ids.imagew.source = "assets/storm.png"

    def show_city_not_found(self):
        self.dialog = MDDialog(
            items=[
                Item(
                    text="City Not Found (404 Error)",
                    source="assets/ladybug.png",
                )
            ],
            type="simple",
            buttons=[
                MDFlatButton(text="cancel", on_release=self.close_dialog)
            ],
        )
        self.dialog.open()

    def close_dialog(self, obj):
        # Close alert box
        self.dialog.dismiss()

    def current_city(self):
        try:
            result = self.callapi(
                f"https://api.ipdata.co/?api-key=3b38bb4e69d7a468ecc91c87a6390fe3b2245e1709dd640e373f2482"
            )
        

            print (result["city"])

            return result["city"]
        except:
            raise
           

    def callapi(self, url):
        try:
            r = requests.get(url=url)
            result = r.json()
            return result
        except requests.ConnectionError:
            self.show_message("Internet connection failed",
                              "assets/ladybug.png")
        except Exception as e:
            self.show_message("Internet connection failed",
                              "assets/ladybug.png")

    def current_cityv2(self):
        soup = BeautifulSoup(
            requests.get(
                f"https://www.google.com/search?q=weather+in+my+current+location"
            ).text,
            "html.parser",
        )
        with open("output1.html", "w", encoding="utf-8") as file:
            file.write(str(soup))

    def show_message(self, text, image):
        self.dialog = MDDialog(
            items=[Item(text=text, source=image)],
            type="simple",
            buttons=[
                MDFlatButton(text="cancel", on_release=self.close_dialog)
            ],
        )
        self.dialog.open()
    

if __name__ == "__main__":
    window = WeatherApp()
    window.run()
