from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QFont, QPixmap, QFontDatabase
from PyQt6.QtCore import QTimer, Qt
from pathlib import Path
from config import API_KEY_WEATHER
import sys
import requests


LAT = 49.4521
LON = 11.0767

def get_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY_WEATHER,
        "units": "metric",
        "lang": "de"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "ort": data["name"],
            "temp": data["main"]["temp"],
            "gefühlte_temp": data["main"]["feels_like"],
            "temp_max": data["main"]["temp_max"],
            "beschreibung": data["weather"][0]["description"].capitalize(),
            "icon": data["weather"][0]["icon"],
            "wind": data["wind"]["speed"]
        }
    except Exception as e:
        return {"error": str(e)}

class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont(
            "/home/nex108/myapiboard/widgets/assets/fonts/PressStart2P-Regular.ttf"
        )
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Layouts
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Text Labels
        self.labels = {
            "ort": QLabel(),
            "temp": QLabel(),
            "beschreibung": QLabel(),
            "wind": QLabel(),
            "error": QLabel()
        }

        for lbl in self.labels.values():
            lbl.setWordWrap(True)
            lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            self.main_layout.addWidget(lbl)

        # Horizontal Layout: Icon | Text
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.icon_label)

        self.text_layout = QVBoxLayout()
        for lbl in self.labels.values():
            self.text_layout.addWidget(lbl)
        self.text_layout.setSpacing(2)

        content_layout.addLayout(self.text_layout)
        self.main_layout.addLayout(content_layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(600_000)
        self.update_weather()

    def resizeEvent(self, event):
        # Dynamische Icon-Größe (max 60% der Widget-Höhe)
        icon_height = int(self.height() * 0.6)
        if self.icon_label.pixmap() and not self.icon_label.pixmap().isNull():
            pixmap = self.icon_label.pixmap()
            scaled = pixmap.scaledToHeight(icon_height, Qt.TransformationMode.SmoothTransformation)
            self.icon_label.setPixmap(scaled)

        # Dynamische Schriftgröße basierend auf Widget-Höhe
        font_size = max(6, int(self.height() * 0.035))  # z. B. 3.5% der Höhe, min. 6
        font = QFont(self.font_family, font_size)
        for lbl in self.labels.values():
            lbl.setFont(font)

        super().resizeEvent(event)

    def update_weather(self):
        data = get_weather()

        if "icon" in data:
            icon_code = data["icon"]
            icon_path = Path(__file__).parent / "assets" / "Weather" / f"{icon_code}.png"
            if icon_path.exists():
                pixmap = QPixmap(str(icon_path))
                self.icon_label.setPixmap(pixmap)
            else:
                self.icon_label.setText("❌ ICON")

        if "error" in data:
            self.labels["error"].setText("❌ FEHLER: " + data["error"].upper())
        else:
            self.labels["ort"].setText(f"📍 {data['ort'].upper()}")
            self.labels["temp"].setText(
                f"🌡 {data['temp']}°C ({data['gefühlte_temp']}°C)\n🔼 {data['temp_max']}°C"
            )
            self.labels["beschreibung"].setText(f"☁️ {data['beschreibung'].upper()}")
            self.labels["wind"].setText(f"💨 WIND: {data['wind']} M/S")
            self.labels["error"].setText("")


