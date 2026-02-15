import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line
from datetime import datetime

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
        container = self.ids.event_container
        container.clear_widgets()
        data = load_data()

        combined = []

        # รวม tasks เป็นแบบ events
        for t in data.get("tasks", []):
            combined.append(
                {
                    "title": t["task"],
                    "date": t.get("date", ""),
                    "time": "",
                    "details": t.get("details", ""),
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

        # เรียงตามวันที่ล่าสุด
        combined.sort(key=lambda x: x["date"], reverse=True)

        if not combined:
            empty_label = Label(
                text="No tasks or events yet.\nAdd one from Calendar!",
                font_size=dp(16),
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(80),
            )
            container.add_widget(empty_label)
            self._combined_events = combined
            return

        for idx, ev in enumerate(combined):
            # การ์ดแต่ละอัน
            card = BoxLayout(
                orientation="vertical", size_hint_y=None, padding=(dp(12), dp(10), dp(12), dp(10)), spacing=dp(6)
            )

            # ความสูงขึ้นอยู่กับรายละเอียด
            card_height = dp(60)  # base
            if ev.get("details"):
                card_height += dp(18)
            card_height += dp(35)  # สำหรับปุ่ม
            card.height = card_height

            # Background
            card.canvas.before.clear()
            with card.canvas.before:
                # พื้นหลัง
                Color(0.97, 0.97, 0.98, 1)
                card.bg = RoundedRectangle(
                    size=card.size,
                    pos=card.pos,
                    radius=[dp(8)]
                )

                # กรอบ
                Color(0.8, 0.8, 0.8, 1)
                card.border = Line(
                    rounded_rectangle=(
                        card.x,
                        card.y,
                        card.width,
                        card.height,
                        dp(8)
                    ),
                    width=1.2
                )

            # อัปเดตตำแหน่ง/ขนาด ทั้ง bg และ border
            def update_canvas(instance, value, card=card):
                card.bg.pos = card.pos
                card.bg.size = card.size
                card.border.rounded_rectangle = (
                    card.x,
                    card.y,
                    card.width,
                    card.height,
                    dp(8)
                )

            card.bind(pos=update_canvas, size=update_canvas)


            



            # ===== HEADER ROW =====
            header = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(25),
                padding=(dp(8), 20, dp(8), 0)  
            )

            # STATUS

            

            status_text = "Done" if ev["done"] else "Pending"
            status_label = Label(
                text=f"{status_text}",
                size_hint_x=None,
                width=dp(80),
                font_size=dp(16),
                color=(0.2, 0.6, 0.3, 1) if ev["done"] else (0.9, 0.2, 0.2, 1)

            )

            # TITLE
            title_label = Label(
                text=ev["title"],
                font_size=dp(14),
                bold=True,
                halign="center",
                valign="middle",
                size_hint_x=1,  
                color = (0, 0, 0, 1)  # light grey

            )
            title_label.bind(width=lambda instance, value: setattr(instance, "text_size", (value, None)))

            # ===== DAY LEFT =====
            countdown_text = ""

            if ev["date"]:
                try:
                    if ev.get("time"):
                        event_datetime = datetime.strptime(
                            f"{ev['date']} {ev['time']}",
                            "%Y-%m-%d %H:%M"
                        )
                    else:
                        event_datetime = datetime.strptime(
                            ev["date"],
                            "%Y-%m-%d"
                        )

                    now = datetime.now()
                    delta = event_datetime - now
                    total_seconds = int(delta.total_seconds())

                    if total_seconds > 0:
                        days = total_seconds // (24 * 3600)
                        hours = (total_seconds % (24 * 3600)) // 3600
                        countdown_text = f"{days} D {hours} H Left"
                    else:
                        countdown_text = "Passed"

                except:
                    countdown_text = ""

            dayleft_label = Label(
                text=f"{countdown_text}" if countdown_text else "",
                size_hint_x=None,
                width=dp(80),
                font_size=dp(16),
                color=(0.3, 0.5, 0.9, 1)
            )

            # ใส่เข้า header
            header.add_widget(status_label)
            header.add_widget(title_label)
            header.add_widget(dayleft_label)

            card.add_widget(header)

            

            # days left
            

            # วันที่และเวลา
            dt_text = ev["date"]
            if ev["time"]:
                dt_text += f" {ev['time']}"
            dt_label = Label(
                text=dt_text,
                font_size=dp(11),
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(18),
            )
            card.add_widget(dt_label)

            # รายละเอียด
            if ev.get("details"):
                det_label = Label(
                    text=ev["details"],
                    font_size=dp(11),
                    color=(0.3, 0.3, 0.3, 1),
                    size_hint_y=None,
                    height=dp(18),
                )
                card.add_widget(det_label)

            # ปุ่มทำเสร็จ / ลบ
            actions = BoxLayout(size_hint_y=None, height=dp(35), spacing=dp(8))

            # Done / Undo
            done_btn = Button(
                text="Done" if not ev["done"] else "Undo",
                background_normal="",
                background_color=(
                    (0.3, 0.7, 0.4, 1) if not ev["done"] else (0.9, 0.9, 0.9, 1)
                ),
                color=(1, 1, 1, 1) if not ev["done"] else (0, 0, 0, 1),
            )
            done_btn.bind(on_press=lambda btn, i=idx: self.mark_done(i))
            actions.add_widget(done_btn)

            # Delete
            del_btn = Button(
                text="Delete",
                background_normal="",
                background_color=(0.88, 0.43, 0.45, 1),
                color=(1, 1, 1, 1),
            )
            del_btn.bind(on_press=lambda btn, i=idx: self.delete_event(i))
            actions.add_widget(del_btn)

            card.add_widget(actions)
            container.add_widget(card)

        # ป้องกันปัญหาความสูงทับกัน
        total_height = sum([child.height for child in container.children]) + dp(
            8
        ) * len(container.children)
        container.height = total_height

        # เก็บ combined events สำหรับ callback
        self._combined_events = combined

    def mark_done(self, index):
        combined = self._combined_events
        item = combined[index]
        data = load_data()

        if item["is_task"]:
            data["tasks"][index]["done"] = not data["tasks"][index]["done"]
        else:
            for i, e in enumerate(data.get("events", [])):
                if e["title"] == item["title"] and e["date"] == item["date"]:
                    data["events"][i]["done"] = not data["events"][i]["done"]
                    break

        save_data(data)
        self.refresh_events()

    def delete_event(self, index):
        combined = self._combined_events
        item = combined[index]
        data = load_data()

        if item["is_task"]:
            del data["tasks"][index]
        else:
            for i, e in enumerate(data.get("events", [])):
                if e["title"] == item["title"] and e["date"] == item["date"]:
                    del data["events"][i]
                    break

        save_data(data)
        self.refresh_events()
