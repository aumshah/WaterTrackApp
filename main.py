import webbrowser

import kivy.core.window
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout

#Config.set('graphics', 'resizable', '0')
#Config.set('graphics', 'width', "393")
#Config.set('graphics', 'height', "852")
#Config.set('graphics', 'width', "1179")
#Config.set('graphics', 'height', "2556")
Config.set('graphics', 'always_on_top', 1)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy import Logger
from datetime import datetime, timedelta
from kivy.uix.spinner import Spinner
from kivy.uix.settings import Settings
from kivy.config import ConfigParser
import time
import os
# venv: site-packages
import numpy
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')
plt.set_loglevel("warning")

print("Welcome to Water Track!")

store = JsonStore("startingStorage.json")
user_data_dir_path = ""
base_json_str = '{"userData": {"units": "gallons"}, "dailyBreakdown": {}, "waterConfiguration": {"showerRate": 2, "faucetRate": 1.5, "hoseRate": 5, "sprinklerRate": 4, "tubRate": 2.5}}'

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

#logging.getLogger('matplotlib.font_manager').disabled = True

# Statistic Graph Update Function
def update_statistics_image():
    values_xaxis = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    kitchenConsumption = []
    appliances = []
    outdoorUse = []
    bathroom = []
    other = []
    # current_date = datetime.now().strftime("%m/%d/%Y")
    current_date = datetime.now()
    idx = (current_date.weekday() + 1) % 7

    sun = current_date - timedelta(idx)
    for i in range(7):
        date = sun.strftime("%m/%d/%Y")
        # values_xaxis.append(date)
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

    plt.clf()
    plt.close()

    matplotlib.use('Agg')
    plt.figure(facecolor=(244 / 255, 251 / 255, 1))
    plt.rcParams.update({'figure.autolayout': True});
    plt.rcParams.update({'font.size': 20, 'font.weight': 'bold'})
    plt.xlabel('Day', weight='bold')
    print("Error after here:")

    plt.bar(values_xaxis, kitchenConsumption, color='lightsteelblue', width=0.75);print(112)
    plt.bar(values_xaxis, appliances, bottom=kitchenConsumption, color='cornflowerblue', width=0.75);print(113)
    plt.bar(values_xaxis, outdoorUse, bottom=[kitchenConsumption[i] + appliances[i] for i in range(7)],color='royalblue', width=0.75);print(114)
    plt.bar(values_xaxis, bathroom, bottom=[kitchenConsumption[i] + appliances[i] + outdoorUse[i] for i in range(7)], color='mediumblue', width=0.75); print(115)
    plt.bar(values_xaxis, other, bottom=[kitchenConsumption[i] + appliances[i] + outdoorUse[i] + bathroom[i] for i in range(7)], color='navy', width=0.75); print(116)
    plt.bar(values_xaxis, [(kitchenConsumption[i] + appliances[i] + outdoorUse[i] + bathroom[i] + other[i]) * 0.05 for i in range(7)], bottom=[kitchenConsumption[i] + appliances[i] + outdoorUse[i] + bathroom[i] for i in range(7)], color='white', width=0.75); print(117)
    print("Plot made!"); print(118)

    plt.savefig(os.path.join(user_data_dir_path, "StatsImage.png")); print(128)
    print("Successfully Saved Image!"); print(129)
    plt.close();
    plt.clf()
    """
    f = plt.figure(facecolor=(244 / 255, 251 / 255, 1)); print(105)
    plt.rcParams.update({'figure.autolayout': True}); print(106)
    ax = f.add_subplot(111); print(107)
    #plt.ylabel('Gallons')
    plt.rcParams.update({'font.size': 20, 'font.weight': 'bold'}); print(109)
    matplotlib.use('Agg')
    ax.set_xlabel('Day', weight='bold'); print(110)

    ax.bar(values_xaxis, [1,1,1,1,1,1,1]); print(111)
    ax.bar(values_xaxis, kitchenConsumption, color='lightsteelblue', width=0.75); print(112)
    ax.bar(values_xaxis, appliances, bottom=kitchenConsumption, color='cornflowerblue', width=0.75); print(113)
    ax.bar(values_xaxis, outdoorUse, bottom=[kitchenConsumption[i]+appliances[i] for i in range(7)], color='royalblue', width=0.75); print(114)
    ax.bar(values_xaxis, bathroom, bottom=[kitchenConsumption[i]+appliances[i]+outdoorUse[i] for i in range(7)], color='mediumblue', width=0.75); print(115)
    ax.bar(values_xaxis, other, bottom=[kitchenConsumption[i]+appliances[i]+outdoorUse[i]+bathroom[i] for i in range(7)], color='navy', width=0.75); print(116)
    ax.bar(values_xaxis, [(kitchenConsumption[i]+appliances[i]+outdoorUse[i]+bathroom[i]+other[i])*0.05 for i in range(7)], bottom=[kitchenConsumption[i] + appliances[i] + outdoorUse[i] + bathroom[i] for i in range(7)], color='white', width=0.75); print(117)
    
    print("Plot made!"); print(126)

    f.savefig(os.path.join(user_data_dir_path,"StatsImage.png")); print(128)
    print("Successfully Saved Image!"); print(129)
    plt.close(f); print(126)
    f.clf()
    """


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
        update_statistics_image()
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_pre_enter(self, *args):
        print("Pre enter Get Started Page")


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
        print("Pre enter home page")
        update_statistics_image()
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
        update_statistics_image()

    def on_pre_enter(self, *args):
        update_statistics_image()
        self.ids.StatsImage.source = os.path.join(user_data_dir_path,"StatsImage.png")
        self.ids.StatsImage.reload()
        self.ids.StatsImage.height =self.parent.parent.width * 0.75
        self.ids.StatsImage.width = self.parent.parent.width
        self.ids.Key.height = self.parent.parent.width * 0.6 * 0.53
        self.ids.Key.width = self.parent.parent.width * 0.6
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        kitchenConsumption = []
        appliances = []
        outdoorUse = []
        bathroom = []
        other = []
        current_date = datetime.now()
        idx = (current_date.weekday() + 1) % 7

        sun = current_date - timedelta(idx)
        for i in range(7):
            date = sun.strftime("%m/%d/%Y")
            # values_xaxis.append(date)
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
    total_time = 0
    waterUsageType = ""
    last_time = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_timer_text, 0.05)

    def timer_dropdown(self, entered_text):
        self.waterUsageType = entered_text

    def restart_press(self, *args):
        self.ids.restartToggleButton.color = (0.5, 0.5, 0.5, 0.5)

    def pause_press(self, *args):
        self.ids.pauseToggleButton.color = (0.5, 0.5, 0.5, 0.5)

    def restart_timer(self, *args):
        self.total_time = 0
        self.ids.restartToggleButton.color = (0.5, 0.5, 0.5, 1)
        self.ids.pauseToggleButton.color = (0, 0, 0, 1)
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
            self.ids.pauseToggleButton.color = (0.5, 0.5, 0.5, 0.5)
            self.timerOn = False
            self.total_time += time.time() - self.last_time
        else:
            self.ids.pauseToggleButton.color = (0, 0, 0, 1)
            self.timerOn = True
            self.last_time = time.time()
        return

    #def update_label(self, *args):
    #    if self.timerOn:
    #        self.sec += 1
    #        self.update_timer_text()

    def update_timer_text(self, *args):
        text = ""
        if self.timerOn:
            self.total_time += time.time() - self.last_time
            self.last_time = time.time()

        num_sec = round(self.total_time)%60
        num_min = round(self.total_time)//60

        if num_min == 0:
            text += "00"
        elif num_min < 10:
            text += "0" + str(num_min)
        else:
            text += str(num_min)

        text += ":"

        if num_sec == 0:
            text += "00"
        elif num_sec < 10:
            text += "0" + str(num_sec)
        else:
            text += str(num_sec)

        self.ids.timer.text = text

    def toggle_timer(self):
        if self.waterUsageType == "" or self.waterUsageType == "Select Usage":
            SelectUsageAlert().open()
            return
        if self.timerOn or self.total_time != 0:
            self.timerOn = False
            self.ids.timerToggleButton.text = str("Start Water Timer")
            self.ids.pauseToggleButton.color = (0.5, 0.5, 0.5, 0.5)
            self.ids.restartToggleButton.color = (0.5, 0.5, 0.5, 0.5)
            WaterTimerPopup().pass_data(round(self.total_time//60), round(self.total_time%60), self.waterUsageType)
            WaterTimerPopup().open()
            self.total_time = 0
            self.update_timer_text()
        else:
            self.timerOn = True
            self.last_time = time.time()
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
        global user_data_dir_path, store, base_json_str

        self.sm = ScreenManager()
        user_data_dir_path = getattr(self, "user_data_dir")
        print(user_data_dir_path)
        store = JsonStore(os.path.join(user_data_dir_path, "storage.json"))

        try:
            if os.stat(os.path.join(user_data_dir_path, "storage.json")).st_size == 0:
                with open(os.path.join(user_data_dir_path, "storage.json"), "w") as f:
                    f.write(base_json_str)
        except Exception as e:
            print(e)
            with open(os.path.join(user_data_dir_path, "storage.json"), "w") as f:
                f.write(base_json_str)
                print("Created file!")
        store = JsonStore(os.path.join(user_data_dir_path, "storage.json"))
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
    Logger.info("Started the app!!")
    print(kivy.core.window.Window.dpi)
    WaterTrackApp().run()
