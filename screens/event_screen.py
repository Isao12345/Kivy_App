import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

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
        self.refresh_events()

    def refresh_events(self):
        """โหลด events + tasks และเพิ่ม widget ลงใน container"""
        container = self.ids.event_container
        container.clear_widgets()

        data = load_data()

        combined = []

        # รวม tasks เป็น event-like dict
        for t in data.get("tasks", []):
            combined.append(
                {
                    "title": t["task"],
                    "date": t.get("date", ""),
                    "time": "",
                    "details": "",
                    "done": t.get("done", False),
                    "is_task": True,
                }
            )

        # รวม events
        for e in data.get("events", []):
            combined.append(
                {
                    "title": e["title"],
                    "date": e.get("date", ""),
                    "time": e.get("time", ""),
                    "details": e.get("details", ""),
                    "done": e.get("done", False),
                    "is_task": False,
                }
            )

        for idx, ev in enumerate(combined):
            row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))

            # แสดงวันเวลา + title
            row.add_widget(Label(text=ev["date"], size_hint_x=None, width=dp(100)))
            row.add_widget(Label(text=ev["title"]))
            row.add_widget(Label(text=ev.get("details", "")))

            # ปุ่ม Done
            done_btn = Button(
                text="✔",
                size_hint_x=None,
                width=dp(50),
                background_normal="",
                background_color=(0.2, 0.7, 0.3, 1),
            )
            done_btn.bind(on_press=lambda btn, i=idx: self.mark_done(i))
            row.add_widget(done_btn)

            # ปุ่ม Delete
            del_btn = Button(
                text="✖",
                size_hint_x=None,
                width=dp(50),
                background_normal="",
                background_color=(0.9, 0.3, 0.3, 1),
            )
            del_btn.bind(on_press=lambda btn, i=idx: self.delete_event(i))
            row.add_widget(del_btn)

            # ถ้า done ให้เปลี่ยนสี background
            if ev["done"]:
                row.opacity = 0.5

            container.add_widget(row)

        # เก็บ combined สำหรับ access ใน mark_done/delete
        self._combined_events = combined

    def mark_done(self, index):
        """เปลี่ยนสถานะ Done ของ task/event"""
        combined = self._combined_events
        item = combined[index]

        data = load_data()

        if item["is_task"]:
            data["tasks"][index]["done"] = not data["tasks"][index]["done"]
        else:
            # index ของ events ต้องหาใน data
            ev_idx = 0
            for i, e in enumerate(data["events"]):
                if e["title"] == item["title"] and e["date"] == item["date"]:
                    ev_idx = i
                    break
            data["events"][ev_idx]["done"] = not data["events"][ev_idx]["done"]

        save_data(data)
        self.refresh_events()

    def delete_event(self, index):
        combined = self._combined_events
        item = combined[index]

        data = load_data()

        if item["is_task"]:
            del data["tasks"][index]
        else:
            # index ของ events ต้องหาใน data
            ev_idx = 0
            for i, e in enumerate(data["events"]):
                if e["title"] == item["title"] and e["date"] == item["date"]:
                    ev_idx = i
                    break
            del data["events"][ev_idx]

        save_data(data)
        self.refresh_events()
