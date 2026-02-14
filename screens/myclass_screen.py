import os
import json
import shutil
from kivy.uix.screenmanager import Screen

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "data.json")
IMAGE_DIR = os.path.join(DATA_DIR, "images")


def load_data():
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump({"tasks": [], "class_image": "", "events": []}, f)
        return {"tasks": [], "class_image": "", "events": []}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump({"tasks": [], "class_image": "", "events": []}, f)
        return {"tasks": [], "class_image": "", "events": []}


def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class MyClassScreen(Screen):
    preview_path = ""  # path ของไฟล์ที่เลือกเพื่อ preview

    def on_enter(self):
        data = load_data()
        image_path = data.get("class_image", "")
        if image_path and os.path.exists(image_path):
            self.ids.class_image.source = image_path
        else:
            self.ids.class_image.source = ""
        self.preview_path = ""  # reset preview

    def select_image(self, selection):
        if not selection:
            return
        self.preview_path = selection[0]
        # แสดง preview ทันที
        self.ids.class_image.source = self.preview_path
        self.ids.class_image.reload()

    def apply_image(self):
        """กดปุ่มนี้เพื่อบันทึกภาพลง data.json และ copy ไปโฟลเดอร์ images"""
        if not self.preview_path:
            return

        os.makedirs(IMAGE_DIR, exist_ok=True)
        filename = os.path.basename(self.preview_path)
        new_path = os.path.join(IMAGE_DIR, filename)
        shutil.copy(self.preview_path, new_path)

        data = load_data()
        data["class_image"] = new_path
        save_data(data)

        self.ids.class_image.source = new_path
        self.ids.class_image.reload()
        self.preview_path = ""  # reset preview
