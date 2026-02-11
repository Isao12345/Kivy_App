from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import calendar
from datetime import datetime
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "data.json")


def load_data():
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except:
        return {"tasks": []}


def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)


class CalendarScreen(Screen):
    def on_enter(self):
        self.ids.calendar_container.clear_widgets()
        self.build_calendar()

    def build_calendar(self):
        now = datetime.now()
        year, month = now.year, now.month

        # แสดงเดือนและปี
        header = Label(
            text=f"{calendar.month_name[month]} {year}",
            font_size=24,
            size_hint_y=None,
            height=40,
        )
        self.ids.calendar_container.add_widget(header)

        # สร้าง grid 7 วัน/สัปดาห์
        grid = GridLayout(cols=7, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        # วันในสัปดาห์
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            grid.add_widget(Label(text=day, bold=True, size_hint_y=None, height=30))

        cal = calendar.monthcalendar(year, month)
        for week in cal:
            for day in week:
                if day == 0:
                    grid.add_widget(Label(text=""))  # ช่องว่าง
                else:
                    btn = Button(text=str(day), size_hint_y=None, height=40)
                    btn.bind(on_press=lambda x, d=day: self.add_task_popup(d))
                    grid.add_widget(btn)

        self.ids.calendar_container.add_widget(grid)

    def add_task_popup(self, day):
        layout = GridLayout(cols=1, padding=10, spacing=10)
        ti = TextInput(hint_text="Enter task", multiline=False)
        layout.add_widget(ti)

        def save_task(instance):
            task_text = ti.text.strip()
            if task_text:
                data = load_data()
                data["tasks"].append(
                    {
                        "task": task_text,
                        "done": False,
                        "date": f"{day}/{datetime.now().month}/{datetime.now().year}",
                    }
                )
                save_data(data)
            popup.dismiss()

        btn = Button(text="Add Task", size_hint_y=None, height=40)
        btn.bind(on_press=save_task)
        layout.add_widget(btn)

        popup = Popup(
            title=f"Add Task for {day}/{datetime.now().month}/{datetime.now().year}",
            content=layout,
            size_hint=(0.7, 0.5),
        )
        popup.open()
