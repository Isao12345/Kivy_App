import os
import json
from datetime import date, timedelta, datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.graphics import Color, RoundedRectangle

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "data.json")

# Month names
MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def load_data():
    if not os.path.exists(DATA_PATH):
        return {"tasks": [], "class_image": "", "events": []}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"tasks": [], "class_image": "", "events": []}


def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class CalendarScreen(Screen):
    current_year = NumericProperty()
    current_month = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month

    def on_enter(self):
        self.draw_calendar()

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.draw_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.draw_calendar()

    def prev_year(self):
        self.current_year -= 1
        self.draw_calendar()

    def next_year(self):
        self.current_year += 1
        self.draw_calendar()

    def draw_calendar(self):
        container: GridLayout = self.ids.days_container
        container.clear_widgets()

        # Update month/year label
        month_name = MONTH_NAMES[self.current_month - 1]
        if hasattr(self.ids, "month_year_label"):
            self.ids.month_year_label.text = f"{month_name} {self.current_year}"
        if hasattr(self.ids, "month_label"):
            self.ids.month_label.text = month_name

        first_day = date(self.current_year, self.current_month, 1)
        start_weekday = first_day.weekday()  # 0=Monday
        # วันสุดท้ายของเดือน
        if self.current_month == 12:
            last_day = date(self.current_year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(self.current_year, self.current_month + 1, 1) - timedelta(
                days=1
            )
        total_days = last_day.day
        today = date.today()

        # ใส่ช่องว่างก่อนวันที่แรก
        for _ in range(start_weekday):
            empty_btn = Button(text="", disabled=True, size_hint_y=None, height=dp(50))
            empty_btn.canvas.before.clear()
            container.add_widget(empty_btn)

        # สร้างปุ่มวันที่
        for day in range(1, total_days + 1):
            day_date = date(self.current_year, self.current_month, day)
            is_today = day_date == today

            day_btn = Button(text=str(day), size_hint_y=None, height=dp(50), background_normal="")

            # Style current day
            if is_today:
                if is_today:
                    day_btn.background_color = (0.65, 0.08, 0.28, 1)
                    day_btn.color = (1, 1, 1, 1)
            # Style others day
            else:
                day_btn.background_color = (0.85, 0.4, 0.6, 1)
                day_btn.color = (1, 1, 1, 1)


            day_btn.bind(on_press=lambda btn, d=day: self.add_task_for_day(d))
            container.add_widget(day_btn)

    def add_task_for_day(self, day):
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button

        popup = Popup(
            title=f"Add Task/Event for {day}/{self.current_month}/{self.current_year}",
            size_hint=(0.8, 0.5),
        )

        layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10))
        title_input = TextInput(hint_text="Title", multiline=False)
        time_input = TextInput(hint_text="HH:MM (optional)", multiline=False)
        details_input = TextInput(hint_text="Details (optional)", multiline=True)

        add_btn = Button(text="Add", size_hint_y=None, height=dp(40))

        def add_task(_):
            title = title_input.text.strip()
            if not title:
                return
            task_date = f"{self.current_year}-{self.current_month:02d}-{day:02d}"

            data = load_data()
            data.setdefault("events", []).append(
                {
                    "title": title,
                    "date": task_date,
                    "time": time_input.text.strip(),
                    "details": details_input.text.strip(),
                    "done": False,
                }
            )
            save_data(data)
            popup.dismiss()

        add_btn.bind(on_press=add_task)
        layout.add_widget(title_input)
        layout.add_widget(time_input)
        layout.add_widget(details_input)
        layout.add_widget(add_btn)

        popup.content = layout
        popup.open()
