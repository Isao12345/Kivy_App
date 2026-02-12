import os
import json
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

# -----------------------------
# Path Data
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "data.json")


# -----------------------------
# Data Functions
# -----------------------------
def load_data():
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except:
        return {"tasks": []}


def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# Task Row
# -----------------------------
class TaskRow(BoxLayout):
    pass


# -----------------------------
# Home Screen
# -----------------------------
class HomeScreen(Screen):

    def on_enter(self):
        self.refresh_tasks()

    def refresh_tasks(self):
        self.ids.active_container.clear_widgets()
        self.ids.done_container.clear_widgets()

        today = datetime.now()
        today_str = f"{today.day}/{today.month}/{today.year}"

        # อัปเดตหัวข้อ Today
        self.ids.today_label.text = f"📅 Today: {today_str}"

        data = load_data()
        self.tasks = data.get("tasks", [])

        for index, task in enumerate(self.tasks):

            # ถ้าไม่มี date ให้ถือว่าเป็นวันนี้
            task_date = task.get("date", today_str)

            if task_date != today_str:
                continue

            row = TaskRow()
            row.ids.task_label.text = task["task"]

            row.ids.done_btn.bind(on_press=lambda x, i=index: self.toggle_done(i))
            row.ids.delete_btn.bind(on_press=lambda x, i=index: self.delete_task(i))

            if task["done"]:
                row.ids.task_label.color = (0.4, 0.4, 0.4, 1)
                self.ids.done_container.add_widget(row)
            else:
                row.ids.task_label.color = (0, 0, 0, 1)
                self.ids.active_container.add_widget(row)

    def add_task(self, text):
        if not text.strip():
            return

        today = datetime.now()
        today_str = f"{today.day}/{today.month}/{today.year}"

        data = load_data()
        data["tasks"].append({"task": text.strip(), "done": False, "date": today_str})

        save_data(data)
        self.ids.new_task_input.text = ""
        self.refresh_tasks()

    def delete_task(self, index):
        data = load_data()
        if index < len(data["tasks"]):
            data["tasks"].pop(index)
            save_data(data)
            self.refresh_tasks()

    def toggle_done(self, index):
        data = load_data()
        if index < len(data["tasks"]):
            data["tasks"][index]["done"] = not data["tasks"][index]["done"]
            save_data(data)
            self.refresh_tasks()
