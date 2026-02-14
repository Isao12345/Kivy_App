import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

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
        """Load events + tasks and add widgets to container"""
        container = self.ids.event_container
        container.clear_widgets()

        data = load_data()

        combined = []

        # Combine tasks as event-like dict
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

        # Combine events
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

        # Sort by date
        combined.sort(key=lambda x: x["date"], reverse=True)

        if not combined:
            # Show empty state
            empty_label = Label(
                text="No tasks or events yet.\nCreate one by clicking a date in Calendar!",
                font_size=dp(16),
                color=(0.5, 0.5, 0.5, 1.0),
                size_hint_y=None,
                height=dp(100),
            )
            container.add_widget(empty_label)
            self._combined_events = combined
            return

        for idx, ev in enumerate(combined):
            # Create card container
            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(90),
                padding=dp(12),
                spacing=dp(8),
            )

            # Style the card
            if ev["done"]:
                bg_color = (0.92, 0.95, 0.97, 1.0)
                card.opacity = 0.6
            else:
                bg_color = (1, 1, 1, 1.0)
                card.opacity = 1.0

            card.canvas.before.clear()
            with card.canvas.before:
                Color(*bg_color)
                RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(8)])
                # Border
                Color(0.88, 0.88, 0.92, 1.0)
                from kivy.graphics import Line

                Line(rectangle=(card.x, card.y, card.width, card.height), width=1)

            # Header with title and time
            header = BoxLayout(size_hint_y=None, height=dp(28), spacing=dp(8))

            # Icon based on type
            icon = "📝" if ev["is_task"] else "📅"
            title_label = Label(
                text=f"{icon} {ev['title']}",
                font_size=dp(14),
                bold=True,
                color=(0.2, 0.2, 0.2, 1.0),
                size_hint_x=0.7,
            )
            header.add_widget(title_label)

            # Date and time info
            info_text = ev["date"]
            if ev["time"]:
                info_text += f" {ev['time']}"

            info_label = Label(
                text=info_text,
                font_size=dp(11),
                color=(0.6, 0.6, 0.6, 1.0),
                size_hint_x=0.3,
            )
            header.add_widget(info_label)
            card.add_widget(header)

            # Details if present
            if ev.get("details", ""):
                details_label = Label(
                    text=ev["details"],
                    font_size=dp(11),
                    color=(0.4, 0.45, 0.5, 1.0),
                    size_hint_y=None,
                    height=dp(18),
                )
                card.add_widget(details_label)

            # Action buttons
            actions = BoxLayout(size_hint_y=None, height=dp(35), spacing=dp(8))

            # Done button
            done_btn = Button(
                text="✓ Done" if not ev["done"] else "✓ Undo",
                size_hint_x=0.5,
                background_color=(
                    (0.29, 0.78, 0.45, 1.0)
                    if not ev["done"]
                    else (0.88, 0.88, 0.92, 1.0)
                ),
            )
            done_btn.canvas.before.clear()
            with done_btn.canvas.before:
                Color(*done_btn.background_color)
                RoundedRectangle(size=done_btn.size, pos=done_btn.pos, radius=[dp(6)])

            done_btn.bind(on_press=lambda btn, i=idx: self.mark_done(i))
            actions.add_widget(done_btn)

            # Delete button
            del_btn = Button(
                text="✕ Delete",
                size_hint_x=0.5,
                background_color=(0.88, 0.43, 0.45, 1.0),
            )
            del_btn.canvas.before.clear()
            with del_btn.canvas.before:
                Color(*del_btn.background_color)
                RoundedRectangle(size=del_btn.size, pos=del_btn.pos, radius=[dp(6)])

            del_btn.bind(on_press=lambda btn, i=idx: self.delete_event(i))
            actions.add_widget(del_btn)

            card.add_widget(actions)
            container.add_widget(card)

        # Store combined for access in mark_done/delete
        self._combined_events = combined

    def mark_done(self, index):
        """Toggle Done status of task/event"""
        combined = self._combined_events
        item = combined[index]

        data = load_data()

        if item["is_task"]:
            if index < len(data["tasks"]):
                data["tasks"][index]["done"] = not data["tasks"][index]["done"]
        else:
            # Find events index
            ev_idx = 0
            for i, e in enumerate(data.get("events", [])):
                if e["title"] == item["title"] and e["date"] == item["date"]:
                    ev_idx = i
                    break
            if ev_idx < len(data.get("events", [])):
                data["events"][ev_idx]["done"] = not data["events"][ev_idx]["done"]

        save_data(data)
        self.refresh_events()

    def delete_event(self, index):
        combined = self._combined_events
        item = combined[index]

        data = load_data()

        if item["is_task"]:
            if index < len(data["tasks"]):
                del data["tasks"][index]
        else:
            # Find events index
            ev_idx = 0
            for i, e in enumerate(data.get("events", [])):
                if e["title"] == item["title"] and e["date"] == item["date"]:
                    ev_idx = i
                    break
            if ev_idx < len(data.get("events", [])):
                del data["events"][ev_idx]

        save_data(data)
        self.refresh_events()
