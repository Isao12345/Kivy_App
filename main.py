import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

# -----------------------
# Import screens
# -----------------------
from screens.home_screen import HomeScreen
from screens.myclass_screen import MyClassScreen
from screens.calendar_screen import CalendarScreen
from screens.event_screen import EventScreen

# -----------------------
# Load KV files
# -----------------------
BASE_DIR = os.path.dirname(__file__)
Builder.load_file(os.path.join(BASE_DIR, "kv/home.kv"))
Builder.load_file(os.path.join(BASE_DIR, "kv/myclass.kv"))
Builder.load_file(os.path.join(BASE_DIR, "kv/calendar.kv"))
Builder.load_file(os.path.join(BASE_DIR, "kv/event.kv"))


# -----------------------
# App
# -----------------------
class StudentLifeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(MyClassScreen(name="myclass"))
        sm.add_widget(CalendarScreen(name="calendar"))
        sm.add_widget(EventScreen(name="event"))
        return sm


if __name__ == "__main__":
    StudentLifeApp().run()
