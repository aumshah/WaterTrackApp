import logging
import webbrowser

from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout

# Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '260')
Config.set('graphics', 'height', '560')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from datetime import datetime, timedelta
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.settings import Settings
from kivy.config import ConfigParser
import numpy as np
import matplotlib.pyplot as plt
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

store = JsonStore("storage.json")

Builder.load_file("pages/CustomClasses.kv")
Builder.load_file('pages/GetStartedPage.kv')
Builder.load_file('pages/HomePage.kv')
Builder.load_file("pages/InfoPage.kv")
Builder.load_file("pages/StatsPage.kv")
Builder.load_file("pages/TimerPage.kv")
Builder.load_file("pages/SettingsPage.kv")
Builder.load_file("pages/BlankPage.kv")
Builder.load_file("popups/WaterTimerPopups.kv")
Builder.load_file("popups/HomePagePopups.kv")

logging.getLogger('matplotlib.font_manager').disabled = True

# Popup classes
class WaterTimerPopup(Popup):
    minUsed = 0
    secUsed = 0
    waterUsageType = ""
    volume = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        return

    @staticmethod
    def pass_data(minutes, sec, w_type):
        WaterTimerPopup.minUsed = minutes
        WaterTimerPopup.secUsed = sec
        WaterTimerPopup.waterUsageType = w_type
        return

    def on_open(self, *args):
        usageType = WaterTimerPopup.waterUsageType
        self.ids.waterUsageInfoTime.text = str("You used " + str(WaterTimerPopup.minUsed) +
                                               " minutes and " + str(WaterTimerPopup.secUsed)
                                               + " seconds of water.\n")

        time = WaterTimerPopup.minUsed + WaterTimerPopup.secUsed / 60
        if usageType == "Shower":
            WaterTimerPopup.volume = round(time * store["waterConfiguration"]["showerRate"],1)
        elif usageType == "Washing Dishes":
            WaterTimerPopup.volume = round(time * store["waterConfiguration"]["faucetRate"],1)
        elif usageType == "Hose":
            WaterTimerPopup.volume = round(time * store["waterConfiguration"]["hoseRate"],1)
        elif usageType == "Sprinkler":
            WaterTimerPopup.volume = round(time * store["waterConfiguration"]["sprinklerRate"],1)
        #elif usageType == "Fill Up Tub":
        #    WaterTimerPopup.volume = round(time * store["waterConfiguration"]["tubRate"],1)

        self.ids.waterUsageInfoVolume.text = str("This is equal to " + str(WaterTimerPopup.volume) +
                                                 " " + store["userData"]["units"] +
                                                 " of water.\n")

    def add(self):
        usage_type = WaterTimerPopup.waterUsageType
        if usage_type == "Shower":
            usage_type = "Bathroom"
        if usage_type == "Washing Dishes":
            usage_type = "Kitchen/Consumption"
        if usage_type == "Hose":
            usage_type = "Outdoor Use"
        if usage_type == "Sprinkler":
            usage_type = "Outdoor Use"
        #if usage_type == "Fill Up Tub":
        #    usage_type = "Outdoor Use"
        current_date = datetime.now().strftime("%m/%d/%Y")
        d1 = store["dailyBreakdown"]
        d2 = d1[current_date]
        if usage_type in d2.keys():
            d2.update(**{usage_type: round(d2[usage_type] + WaterTimerPopup.volume, 1)})
        else:
            d2.update(**{usage_type: round(WaterTimerPopup.volume, 1)})
        d1.update(**{current_date: d2})
        store.put("dailyBreakdown", **d1)
        self.dismiss()


class SelectUsageAlert(Popup):
    pass

class EnterANumberAlert(Popup):
    pass

class AddWaterUsagePopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        return

    def usage_selected(self, usage):
        self.ids.exactWaterUsageSpinner.opacity = 1
        if usage == "Appliances":
            self.ids.exactWaterUsageSpinner.values = ["Dishwasher", "Washing Machine"]
        elif usage == "Kitchen/Consumption":
            self.ids.exactWaterUsageSpinner.values = ["Drinking Water", "Hand Washing Dishes", "Ice", "Coffee/Tea", "Washing Hands",
                                                      "Cooking"]
        elif usage == "Bathroom":
            self.ids.exactWaterUsageSpinner.values = ["Shower/Bath", "Toilet", "Washing Hands", "Washing Face",
                                                      "Brushing Teeth"]
        elif usage == "Outdoor Use":
            self.ids.exactWaterUsageSpinner.values = ["Hose", "Sprinkler", "Car Wash", "Dog Bath"]
        elif usage == "Other":
            self.ids.exactWaterUsageSpinner.values = ["Other"]
        return

    def specific_usage_selected(self, usage):
        self.ids.enterUsageLabel.opacity = 1
        self.ids.enterUsageInput.opacity = 1
        if usage == "Dishwasher":
            self.ids.enterUsageLabel.text = "How long (in minutes) was it run?"
            pass
        elif usage == "Washing Machine":
            self.ids.enterUsageLabel.text = "How long (in minutes) was it run?"
            pass
        elif usage == "Drinking Water":
            self.ids.enterUsageLabel.text = "How many glasses did you drink?"
            pass
        elif usage == "Ice":
            self.ids.enterUsageLabel.text = "How many cups of ice did you use?"
            pass
        elif usage == "Coffee/Tea":
            self.ids.enterUsageLabel.text = "How many cups of water did you use?"
            pass
        elif usage == "Washing Hands":
            self.ids.enterUsageLabel.text = "How many seconds did you wash your hands for?"
            pass
        elif usage == "Cooking":
            self.ids.enterUsageLabel.text = "How many cups of water did you use?"
            pass
        elif usage == "Shower/Bath":
            self.ids.enterUsageLabel.text = "How long was the water running (in minutes)?"
            pass
        elif usage == "Toilet":
            self.ids.enterUsageLabel.text = "How many times did you flush?"
            pass
        elif usage == "Washing Face":
            self.ids.enterUsageLabel.text = "How long was the water running (in minutes)?"
            pass
        elif usage == "Brushing Teeth":
            self.ids.enterUsageLabel.text = "How long was the water running (in minutes)?"
            pass
        elif usage == "Hose":
            self.ids.enterUsageLabel.text = "How long was the water running (in minutes)?"
            pass
        elif usage == "Sprinkler":
            self.ids.enterUsageLabel.text = "How long was the water running (in minutes)?"
            pass
        elif usage == "Car Wash":
            self.ids.enterUsageLabel.text = "How long was the water running (in minutes)?"
            pass
        elif usage == "Dog Bath":
            self.ids.enterUsageLabel.text = "How long was the water running (in minutes)?"
            pass
        elif usage == "Other":
            self.ids.enterUsageLabel.text = "Please approximate the number of gallons used"
            pass

        return

    def add(self):
        if self.ids.enterUsageInput.text == "":
            SelectUsageAlert().open()
        try:
            input = float(self.ids.enterUsageInput.text)
            vol = 0
            usage = self.ids.exactWaterUsageSpinner.text
            if usage == "Dishwasher":
                usage_type = "Kitchen/Consumption"
                vol = 4
                pass
            elif usage == "Washing Machine":
                usage_type = "Appliances"
                if input > 15:
                    vol = 25
                else:
                    vol = 15
                pass
            elif usage == "Drinking Water":
                usage_type = "Kitchen/Consumption"
                vol = input * 0.06
                pass
            elif usage == "Ice":
                usage_type = "Kitchen/Consumption"
                vol = input * 0.06
                pass
            elif usage == "Coffee/Tea":
                usage_type = "Kitchen/Consumption"
                vol = input * 0.06
                pass
            elif usage == "Washing Hands":
                usage_type = "Bathroom"
                vol = (input/60) * store["waterConfiguration"]["faucetRate"]
                pass
            elif usage == "Cooking":
                usage_type = "Kitchen/Consumption"
                vol = input * 0.06
                pass
            elif usage == "Shower/Bath":
                usage_type = "Bathroom"
                vol = input * store["waterConfiguration"]["showerRate"]
                pass
            elif usage == "Toilet":
                usage_type = "Bathroom"
                vol = input * 2
                pass
            elif usage == "Washing Face":
                usage_type = "Bathroom"
                vol = input * store["waterConfiguration"]["faucetRate"]
                pass
            elif usage == "Brushing Teeth":
                usage_type = "Bathroom"
                vol = input * store["waterConfiguration"]["faucetRate"]
                pass
            elif usage == "Hose":
                usage_type = "Outdoor Use"
                vol = input * store["waterConfiguration"]["hoseRate"]
                pass
            elif usage == "Sprinkler":
                usage_type = "Outdoor Use"
                vol = input * store["waterConfiguration"]["sprinklerRate"]
                pass
            elif usage == "Car Wash":
                usage_type = "Outdoor Use"
                vol = input * store["waterConfiguration"]["hoseRate"]
                pass
            elif usage == "Dog Bath":
                usage_type = "Outdoor Use"
                vol = input * store["waterConfiguration"]["hoseRate"]
                pass
            elif usage == "Other":
                usage_type = "Other"
                vol = input
                pass

            current_date = datetime.now().strftime("%m/%d/%Y")
            d1 = store["dailyBreakdown"]
            d2 = d1[current_date]
            if usage_type in d2.keys():
                d2.update(**{usage_type: round(d2[usage_type] + vol, 1)})
            else:
                d2.update(**{usage_type: round(vol, 1)})
            d1.update(**{current_date: d2})
            store.put("dailyBreakdown", **d1)

        except Exception as e:
            EnterANumberAlert().open()
            print(e)
        else:
            pass
        pass
# Classes for different pages in the app + WindowManager
class GetStartedPage(Screen):
    pass


class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        now = datetime.now()
        hour = now.hour
        if 4 <= hour < 12:
            text = "Good morning"
        elif 12 <= hour < 17:
            text = "Good afternoon"
        else:
            text = "Good evening"

        self.ids.greetingText.text = str(text)
        current_date = datetime.now().strftime("%m/%d/%Y")
        self.ids.totalWaterUsage.text = str(round(sum(store["dailyBreakdown"][current_date].values()), 1)) + ' gal.'

    def on_pre_enter(self, *args):
        self.update()

    def update(self):
        current_date = datetime.now().strftime("%m/%d/%Y")
        self.ids.totalWaterUsage.text = str(round(sum(store["dailyBreakdown"][current_date].values()), 1)) + ' gal.'
        today_usage = store["dailyBreakdown"][current_date]

        while True:
            try:
                self.ids.breakdownLabels.remove_widget(self.ids.breakdownLabels.children[0])
            except:
                break

        for usage, vol in today_usage.items():
            if usage == "Kitchen/Consumption":
                usage = "Kitchen/\nConsumption"
            label = BreakDownLabel(u_type=usage, u_volume=vol)
            self.ids.breakdownLabels.add_widget(label)
            pass

        print(today_usage)

    @staticmethod
    def add_usage_click():
        AddWaterUsagePopup().open()

    pass


class InfoPage(Screen):
    def donate(self):
        webbrowser.open("https://givebutter.com/powerofcleanwater")
    pass


class StatsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        values_xaxis = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        kitchenConsumption = []
        appliances = []
        outdoorUse = []
        bathroom = []
        other = []
        #current_date = datetime.now().strftime("%m/%d/%Y")
        current_date = datetime.now()
        idx = (current_date.weekday() + 1) % 7

        sun = current_date - timedelta(idx)
        for i in range(7):
            date = sun.strftime("%m/%d/%Y")
            #values_xaxis.append(date)
            try:
                kitchenConsumption.append(store["dailyBreakdown"][date]["Kitchen/Consumption"])
            except:
                kitchenConsumption.append(0)

            try:
                appliances.append(store["dailyBreakdown"][date]["Appliances"])
            except:
                appliances.append(0)

            try:
                outdoorUse.append(store["dailyBreakdown"][date]["Outdoor Use"])
            except:
                outdoorUse.append(0)

            try:
                bathroom.append(store["dailyBreakdown"][date]["Bathroom"])
            except:
                bathroom.append(0)

            try:
                other.append(store["dailyBreakdown"][date]["Other"])
            except:
                other.append(0)
            sun = sun + timedelta(days=1)
        print(values_xaxis)
        print(kitchenConsumption)
        print(appliances)
        print(outdoorUse)
        print(bathroom)
        print(other)
        plt.figure(facecolor=(244 / 255, 251 / 255, 1))
        #plt.ylabel('Gallons')
        plt.xlabel('Day')
        plt.bar(values_xaxis, kitchenConsumption, color='lightsteelblue', width=0.75)
        plt.bar(values_xaxis, appliances, bottom=kitchenConsumption, color='cornflowerblue', width=0.75)
        plt.bar(values_xaxis, outdoorUse, bottom=[kitchenConsumption[i]+appliances[i] for i in range(7)], color='royalblue', width=0.75)
        plt.bar(values_xaxis, bathroom, bottom=[kitchenConsumption[i]+appliances[i]+outdoorUse[i] for i in range(7)], color='mediumblue', width=0.75)
        plt.bar(values_xaxis, other, bottom=[kitchenConsumption[i]+appliances[i]+outdoorUse[i]+bathroom[i] for i in range(7)], color='navy', width=0.75)

        #plt.title("This Week's Water Usage")
        #plt.legend(["Kitchen/Consumption", "Appliances", "Outdoor Use", "Bathroom", "Other"])
        plt.rcParams.update({'font.size': 1})
        #plt.show()
        self.ids.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()), index=0)

        sum_water_week = [kitchenConsumption[i]+appliances[i]+outdoorUse[i]+bathroom[i]+other[i] for i in range(7)]
        avg_water_usage = round(sum(sum_water_week)/7, 1)
        max_water_usage = max(sum_water_week)
        min_water_usage = min(sum_water_week)
        day_max = days[sum_water_week.index(max_water_usage)]
        day_min = days[sum_water_week.index(min_water_usage)]
        self.ids.avg.text = "Your average water usage this week was " + str(avg_water_usage) + " gal"
        self.ids.max.text = "Your highest usage was " + str(max_water_usage) + " gal on " + day_max
        self.ids.min.text = "Your lowest usage was " + str(min_water_usage) + " gal on " + day_min


class TimerPage(Screen):
    timerOn = False
    min = 0
    sec = 0
    waterUsageType = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_label, 1)

    def timer_dropdown(self, entered_text):
        self.waterUsageType = entered_text

    def restart_press(self, *args):
        self.ids.restartToggleButton.color = (0.5, 0.5, 0.5, 0.5)

    def pause_press(self, *args):
        self.ids.pauseToggleButton.color = (0.5, 0.5, 0.5, 0.5)

    def restart_timer(self, *args):
        self.sec = 0
        self.min = 0
        self.ids.restartToggleButton.color = (0.5, 0.5, 0.5, 1)
        if self.timerOn:
            self.update_timer_text()
            self.timerOn = False
            self.ids.timerToggleButton.text = "Start Water Timer"
            return
        else:
            self.ids.timerToggleButton.text = "Start Water Timer"
            self.update_timer_text()
            return

    def pause_timer(self, *args):
        if self.timerOn:
            self.ids.pauseToggleButton.color = (0.5, 0.5, 0.5, 1)
            self.timerOn = False
        else:
            self.timerOn = True
        return

    def update_label(self, *args):
        if self.timerOn:
            self.sec += 1
            self.update_timer_text()

    def update_timer_text(self):
        text = ""
        if self.sec == 60:
            self.min += 1
            self.sec = 0

        if self.min == 0:
            text += "00"
        elif self.min < 10:
            text += "0" + str(self.min)
        else:
            text += str(self.min)

        text += ":"

        if self.sec == 0:
            text += "00"
        elif self.sec < 10:
            text += "0" + str(self.sec)
        else:
            text += str(self.sec)

        self.ids.timer.text = text

    def toggle_timer(self):
        if self.waterUsageType == "" or self.waterUsageType == "Select Usage":
            SelectUsageAlert().open()
            return
        if self.timerOn or self.min != 0 or self.sec != 0:
            self.timerOn = False
            self.ids.timerToggleButton.text = str("Start Water Timer")
            self.ids.pauseToggleButton.color = (0.5, 0.5, 0.5, 0.5)
            self.ids.restartToggleButton.color = (0.5, 0.5, 0.5, 0.5)
            WaterTimerPopup().pass_data(self.min, self.sec, self.waterUsageType)
            WaterTimerPopup().open()
            self.min = 0
            self.sec = 0
            self.update_timer_text()
        else:
            self.timerOn = True
            self.ids.timerToggleButton.text = str("Stop Water Timer")
            self.ids.pauseToggleButton.color = (0, 0, 0, 1)
            self.ids.restartToggleButton.color = (0, 0, 0, 1)

    pass


class SettingsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = ConfigParser()
        config.read('config.ini')

        s = Settings()
        s.add_json_panel("Settings", config,"settingsFormat.json")

        self.add_widget(s)
        return
    pass

class BlankPage(Screen):
    pass

class WindowManager(ScreenManager):
    pass


# Other classes
class ImageButton(ButtonBehavior, Image):
    pass


class CustomSpinner(Spinner):
    pass

class BreakDownLabel(BoxLayout):
    pass

class WaterTrackApp(App):
    def build(self):
        self.sm = ScreenManager()
        if len(store["dailyBreakdown"].keys()) == 0:
            self.sm.add_widget(GetStartedPage(name="GetStarted"))

        current_date = datetime.now().strftime("%m/%d/%Y")
        if current_date not in store["dailyBreakdown"].keys():
            # This is how you store data in the dictionary
            d1 = store["dailyBreakdown"]
            d1.update(**{current_date: {}})
            store.put("dailyBreakdown", **d1)

        self.sm.add_widget(HomePage(name="HomePage"))
        self.sm.add_widget(InfoPage(name="InfoPage"))
        self.sm.add_widget(StatsPage(name="StatsPage"))
        self.sm.add_widget(TimerPage(name="TimerPage"))
        self.sm.add_widget(SettingsPage(name="SettingsPage"))
        self.sm.add_widget(BlankPage(name="BlankPage"))
        self.icon = r"\img\PowerOfWaterIcon.png"
        return self.sm


if __name__ == '__main__':
    WaterTrackApp().run()
