import os
import json
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "data.json")


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


class EventScreen(Screen):

    def on_enter(self):
        # ใช้ Clock.schedule_once เพื่อให้ ids โหลดเสร็จก่อนเรียก refresh
        Clock.schedule_once(lambda dt: self.refresh_events(), 0)

    def refresh_events(self):
        """โหลดและแสดง events ใน container"""
        container = self.ids.event_container
        container.clear_widgets()

        data = load_data()
        for idx, ev in enumerate(data.get("events", [])):
            row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))

            # แสดงข้อมูล event
            row.add_widget(
                Label(
                    text=f"{ev['date']} {ev['time']}", size_hint_x=None, width=dp(130)
                )
            )
            row.add_widget(Label(text=ev["title"]))
            row.add_widget(Label(text=ev.get("details", "")))

            # ปุ่มแก้ไข
            edit_btn = Button(
                text="✎",
                size_hint_x=None,
                width=dp(40),
                background_normal="",
                background_color=(0.9, 0.9, 0.4, 1),
            )
            edit_btn.bind(on_press=lambda btn, i=idx: self.edit_event(i))
            row.add_widget(edit_btn)

            # ปุ่มลบ
            del_btn = Button(
                text="✖",
                size_hint_x=None,
                width=dp(40),
                background_normal="",
                background_color=(0.9, 0.3, 0.3, 1),
            )
            del_btn.bind(on_press=lambda btn, i=idx: self.delete_event(i))
            row.add_widget(del_btn)

            container.add_widget(row)

    def add_event(self, title, date, time, details):
        """เพิ่ม event ใหม่"""
        if not title.strip():
            return  # ไม่เพิ่มถ้าไม่มีชื่อ event

        data = load_data()
        data.setdefault("events", []).append(
            {"title": title, "date": date, "time": time, "details": details}
        )
        save_data(data)
        self.refresh_events()

        # ล้าง TextInput
        self.ids.event_title.text = ""
        self.ids.event_date.text = ""
        self.ids.event_time.text = ""
        self.ids.event_details.text = ""

    def edit_event(self, index):
        """นำข้อมูล event เดิมไปใส่ใน TextInput เพื่อแก้ไข"""
        data = load_data()
        ev = data["events"][index]

        self.ids.event_title.text = ev["title"]
        self.ids.event_date.text = ev["date"]
        self.ids.event_time.text = ev["time"]
        self.ids.event_details.text = ev.get("details", "")

        # ลบ event เก่าออกก่อน แล้วเพิ่มใหม่เมื่อกด add
        del data["events"][index]
        save_data(data)
        self.refresh_events()

    def delete_event(self, index):
        """ลบ event"""
        data = load_data()
        del data["events"][index]
        save_data(data)
        self.refresh_events()
