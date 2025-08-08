import os
import requests
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from config import API_KEY_NASA


NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"


def get_apod_data():
    params = {
        "api_key": API_KEY_NASA,
        "thumbs": True
    }
    try:
        response = requests.get(NASA_APOD_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Falls kein Bild vorhanden ist (z. B. Video)
        if data.get("media_type") != "image":
            return {
                "title": data.get("title", "Kein Bild verfügbar"),
                "image_url": None
            }

        return {
            "title": data.get("title", "Kein Titel"),
            "image_url": data.get("hdurl") or data.get("url")
        }
    except Exception as e:
        return {"error": str(e)}


class NasaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌌 NASA Bild des Tages")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_title = QLabel()
        self.label_title.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.label_title.setWordWrap(True)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.image_label)
        layout.addWidget(self.label_title)

        self.setLayout(layout)
        self.update_apod()
        

    def resizeEvent(self, event):
        self.scale_pixmap()
        super().resizeEvent(event)  
   
   
    def scale_pixmap(self):
        if hasattr(self, "original_pixmap") and self.original_pixmap and not self.original_pixmap.isNull():
            available_height = int(self.height() * 0.75)  # z. B. max 75 % vom Widget
            scaled = self.original_pixmap.scaledToHeight(
                available_height, Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
   

    def update_apod(self):
        data = get_apod_data()

        if "error" in data:
            self.label_title.setText("❌ Fehler beim Laden")
            self.image_label.clear()
            self.original_pixmap = None
            return

        self.label_title.setText(data["title"])

        if data.get("image_url"):
            try:
                img_response = requests.get(data["image_url"], timeout=10)
                img_response.raise_for_status()
                pixmap = QPixmap()
                pixmap.loadFromData(img_response.content)
                
                self.original_pixmap = pixmap
                self.scale_pixmap()
            except Exception:
                self.image_label.setText("❌ Bild konnte nicht geladen werden.")
                self.original_pixmap = None
        else:
            self.image_label.clear()
            self.original_pixmap = None

