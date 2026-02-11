import os
import json
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
# Task Row Widget
# -----------------------------
class TaskRow(BoxLayout):
    def set_background(self, done: bool):
        """เปลี่ยนสี Label ตามสถานะ task"""
        if done:
            self.ids.task_label.color = (0.4, 0.4, 0.4, 1)  # สีเทา
        else:
            self.ids.task_label.color = (0, 0, 0, 1)  # สีดำ


# -----------------------------
# Home Screen
# -----------------------------
class HomeScreen(Screen):

    def on_enter(self):
        self.refresh_tasks()

    def refresh_tasks(self):
        """โหลด task จาก data.json และเพิ่มลง Active / Done"""
        self.ids.active_container.clear_widgets()
        self.ids.done_container.clear_widgets()

        data = load_data()
        self.tasks = data.get("tasks", [])

        for index, task in enumerate(self.tasks):
            row = TaskRow()
            row.ids.task_label.text = task["task"]
            row.set_background(task["done"])

            # bind ปุ่ม
            row.ids.done_btn.bind(on_press=lambda x, i=index: self.toggle_done(i))
            row.ids.delete_btn.bind(on_press=lambda x, i=index: self.delete_task(i))

            # เพิ่มลง container
            if task["done"]:
                self.ids.done_container.add_widget(row)
            else:
                self.ids.active_container.add_widget(row)

    def add_task(self, text):
        """เพิ่ม task ใหม่"""
        if not text.strip():
            return

        data = load_data()
        data["tasks"].append({"task": text.strip(), "done": False})
        save_data(data)

        self.ids.new_task_input.text = ""
        self.refresh_tasks()

    def delete_task(self, index):
        """ลบ task"""
        data = load_data()
        if index < len(data["tasks"]):
            data["tasks"].pop(index)
            save_data(data)
            self.refresh_tasks()

    def toggle_done(self, index):
        """สลับสถานะ done / active"""
        data = load_data()
        if index >= len(data["tasks"]):
            return

        data["tasks"][index]["done"] = not data["tasks"][index]["done"]
        save_data(data)
        self.refresh_tasks()
