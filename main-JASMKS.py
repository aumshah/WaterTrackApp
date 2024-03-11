from kivy.config import Config

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
from datetime import datetime
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.label import Label

store = JsonStore("storage.json")

Builder.load_file("pages/CustomClasses.kv")
Builder.load_file('pages/GetStartedPage.kv')
Builder.load_file('pages/HomePage.kv')
Builder.load_file("pages/InfoPage.kv")
Builder.load_file("pages/StatsPage.kv")
Builder.load_file("pages/TimerPage.kv")
Builder.load_file("pages/SettingsPage.kv")
Builder.load_file("popups/WaterTimerPopups.kv")
Builder.load_file("popups/HomePagePopups.kv")


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
        self.ids.waterUsageInfoVolume.text = str("This is equal to " + str(WaterTimerPopup.volume) +
                                                 " " + store["userData"]["units"] +
                                                 " of water.\n")

    def add(self):
        usageType = WaterTimerPopup.waterUsageType
        current_date = datetime.now().strftime("%m/%d/%Y")
        d1 = store["dailyBreakdown"]
        d2 = d1[current_date]
        if usageType in d2.keys():
            d2.update(**{usageType: round(d2[usageType] + WaterTimerPopup.volume, 1)})
        else:
            d2.update(**{usageType: round(WaterTimerPopup.volume, 1)})
        d1.update(**{current_date: d2})
        store.put("dailyBreakdown", **d1)
        self.dismiss()



class WaterTimerAlert(Popup):
    pass


class AddWaterUsagePopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        return

    def usage_selected(self, usage):
        if usage == "Appliances" or usage == "Kitchen/Consumption" or usage == "Bathroom" or usage == "Outdoor Use":
            if "exactWaterUsageSpinner" not in self.ids:
                exactSpinner = ExactWaterUsageSpinner()
                self.ids.b_layout.remove_widget(self.ids["positioningLabel"])
                self.ids.b_layout.add_widget(exactSpinner)
                self.ids["exactWaterUsageSpinner"] = exactSpinner
                self.ids.b_layout.add_widget(Widget())
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
            return

    @staticmethod
    def specific_usage_selected(usage):
        if usage == "Dishwasher":
            pass
        elif usage == "Washing Machine":
            pass
        elif usage == "Drinking Water":
            pass
        elif usage == "Ice":
            pass
        elif usage == "Coffee/Tea":
            pass
        elif usage == "Washing Hands":
            pass
        elif usage == "Cooking":
            pass
        elif usage == "Shower/Bath":
            pass
        elif usage == "Toilet":
            pass
        elif usage == "Washing Face":
            pass
        elif usage == "Brushing Teeth":
            pass
        elif usage == "Hose":
            pass
        elif usage == "Sprinkler":
            pass
        elif usage == "Car Wash":
            pass
        elif usage == "Dog Bath":
            pass
        return


# Classes for different pages in the app + WindowManager
class GetStartedPage(Screen):
    pass


class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        now = datetime.now()
        hour = now.hour
        if 4 <= hour < 12:
            text = "Good morning " + store['userData']['name']
        elif 12 <= hour < 17:
            text = "Good afternoon " + store['userData']['name']
        else:
            text = "Good evening " + store['userData']['name']

        self.ids.greetingText.text = str(text)
        current_date = datetime.now().strftime("%m/%d/%Y")
        self.ids.totalWaterUsage.text = str(round(sum(store["dailyBreakdown"][current_date].values()), 1)) + ' gal.'

    def on_enter(self, *args):
        current_date = datetime.now().strftime("%m/%d/%Y")
        self.ids.totalWaterUsage.text = str(round(sum(store["dailyBreakdown"][current_date].values()), 1)) + ' gal.'

        today_usage = store["dailyBreakdown"][current_date]

        print(today_usage)

    @staticmethod
    def add_usage_click():
        AddWaterUsagePopup().open()

    pass


class InfoPage(Screen):
    pass


class StatsPage(Screen):
    pass


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
            WaterTimerAlert().open()
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
    pass


class WindowManager(ScreenManager):
    pass


# Other classes
class ImageButton(ButtonBehavior, Image):
    pass


class CustomSpinner(Spinner):
    pass

class BreakDownLabel(Label):
    pass


class ExactWaterUsageSpinner(CustomSpinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        return

    @staticmethod
    def selected_usage(usage):
        AddWaterUsagePopup().specific_usage_selected(usage)

    pass


class WaterTrackApp(App):
    def build(self):
        current_date = datetime.now().strftime("%m/%d/%Y")
        if current_date not in store["dailyBreakdown"].keys():
            # This is how you store data in the dictionary
            d1 = store["dailyBreakdown"]
            d1.update(**{current_date: {}})
            store.put("dailyBreakdown", **d1)
        sm = ScreenManager()
        sm.add_widget(GetStartedPage(name="GetStarted"))
        sm.add_widget(HomePage(name="HomePage"))
        sm.add_widget(InfoPage(name="InfoPage"))
        sm.add_widget(StatsPage(name="StatsPage"))
        sm.add_widget(TimerPage(name="TimerPage"))
        sm.add_widget(SettingsPage(name="SettingsPage"))
        self.icon = r"\img\PowerOfWaterIcon.png"
        return sm


if __name__ == '__main__':
    WaterTrackApp().run()
