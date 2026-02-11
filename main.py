from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import os
import json

# Paths สำหรับไฟล์ kv และ data
BASE_DIR = os.path.dirname(__file__)
KV_PATH = os.path.join(BASE_DIR, "kv", "home.kv")
DATA_PATH = os.path.join(BASE_DIR, "data", "data.json")

# โหลด layout
Builder.load_file(KV_PATH)


class HomeScreen(Screen):
    def on_enter(self):
        self.load_tasks()

    def load_tasks(self):
        """โหลด tasks จาก data.json และอัพเดต UI"""
        try:
            with open(DATA_PATH, "r") as f:
                data = json.load(f)
            self.tasks = data.get("tasks", [])
        except:
            self.tasks = []
        self.update_ui()

    def update_ui(self):
        """อัพเดต Label แสดง tasks"""
        tasks_str = ", ".join([t["task"] for t in self.tasks])
        self.ids.tasks_label.text = f"Tasks: {tasks_str}"

    def add_task(self, task_text):
        """เพิ่ม task ใหม่"""
        if not task_text:
            return
        self.tasks.append({"task": task_text, "done": False})
        self.save_data()
        self.update_ui()

    def save_data(self):
        """บันทึก tasks ลง data.json"""
        data = {"tasks": self.tasks}
        with open(DATA_PATH, "w") as f:
            json.dump(data, f, indent=4)


class StudentLifeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        return sm


if __name__ == "__main__":
    StudentLifeApp().run()
