from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.metrics import dp
import os
import json

# Paths สำหรับไฟล์ kv และ data
BASE_DIR = os.path.dirname(__file__)
KV_PATH = os.path.join(BASE_DIR, "kv", "home.kv")
DATA_PATH = os.path.join(BASE_DIR, "data", "data.json")

# โหลด layout
Builder.load_file(KV_PATH)


# -----------------------------
# Data Manager (โหลด/บันทึก data.json)
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
# Home Screen
# -----------------------------
class HomeScreen(Screen):
    def on_enter(self):
        self.load_tasks()

    def load_tasks(self):
        """โหลด tasks จาก data.json และอัพเดต UI"""
        data = load_data()
        self.tasks = data.get("tasks", [])
        self.update_ui()

    def update_ui(self):
        """อัพเดต Label แสดง tasks"""
        if self.tasks:
            tasks_str = "\n".join([f"- {t['task']}" for t in self.tasks])
        else:
            tasks_str = "No tasks yet."
        self.ids.tasks_label.text = f"Tasks:\n{tasks_str}"

    def add_task(self, task_text):
        """เพิ่ม task ใหม่"""
        if not task_text.strip():
            return
        self.tasks.append({"task": task_text.strip(), "done": False})
        save_data({"tasks": self.tasks})
        self.update_ui()


# -----------------------------
# App
# -----------------------------
class StudentLifeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        return sm


if __name__ == "__main__":
    StudentLifeApp().run()
