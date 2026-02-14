import os
import json
import shutil
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "data.json")
IMAGE_DIR = os.path.join(DATA_DIR, "images")


def load_data():
    """โหลดข้อมูลจาก data.json"""
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
    """บันทึกข้อมูลลง data.json"""
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
        self.preview_path = ""

    def select_image(self, selection):
        """เลือกไฟล์แล้ว preview ทันที"""
        if not selection:
            return
        self.preview_path = selection[0]
        self.ids.class_image.source = self.preview_path
        self.ids.class_image.reload()

    def apply_image(self):
        """บันทึกรูปลงโฟลเดอร์ images และอัปเดต data.json"""
        if not self.preview_path:
            return

        os.makedirs(IMAGE_DIR, exist_ok=True)
        filename = os.path.basename(self.preview_path)

        # ป้องกันไฟล์ชื่อซ้ำ
        new_path = os.path.join(IMAGE_DIR, filename)
        counter = 1
        while os.path.exists(new_path):
            name, ext = os.path.splitext(filename)
            new_path = os.path.join(IMAGE_DIR, f"{name}_{counter}{ext}")
            counter += 1

        shutil.copy(self.preview_path, new_path)

        data = load_data()

        # ลบรูปเก่า
        old_image = data.get("class_image")
        if old_image and os.path.exists(old_image):
            try:
                os.remove(old_image)
            except Exception:
                pass

        data["class_image"] = new_path
        save_data(data)

        self.ids.class_image.source = new_path
        self.ids.class_image.reload()
        self.preview_path = ""

    def delete_image(self):
        """ลบรูปที่บันทึกไว้"""
        data = load_data()
        image_path = data.get("class_image")

        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception:
                pass

        data["class_image"] = ""
        save_data(data)

        self.ids.class_image.source = ""
        self.ids.class_image.reload()
        self.preview_path = ""

    # ------------------ 🔥 Zoom Fullscreen ------------------
    def open_fullscreen(self):
        image_path = self.ids.class_image.source
        if not image_path:
            return

        layout = BoxLayout()
        layout.orientation = "vertical"

        # พื้นหลังดำ
        with layout.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Image
        full_image = Image(source=image_path, allow_stretch=True, keep_ratio=True)
        layout.add_widget(full_image)

        # ปุ่ม X มุมบน
        close_btn = Button(
            text="✕",
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={"top": 1, "right": 1},
            background_normal="",
            background_color=(0.88, 0.43, 0.45, 1),
            color=(1, 1, 1, 1),
        )
        popup = Popup(
            content=layout, size_hint=(1, 1), auto_dismiss=True, background=""
        )
        close_btn.bind(on_press=popup.dismiss)
        layout.add_widget(close_btn)

        popup.open()

    def _update_rect(self, instance, value):
        """ปรับขนาด background ของ popup"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
