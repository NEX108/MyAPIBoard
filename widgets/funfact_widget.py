import requests
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt, QTimer
from pathlib import Path


def get_fun_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("text", "No fact found.")
    except Exception as e:
        return f"❌ Fehler: {str(e)}"
        
        
def wrap_text(text, max_chars_per_line):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)


class FunFactWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Fun Fact")
        self.setMinimumWidth(300)
        
        #Pixel Font
        font_path = Path(__file__).parent / "assets" / "fonts" / "PressStart2P-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.pixel_font_family = font_family
        
        #Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        #Labels
        self.labels = []

        self.label_title = QLabel("🧠 Fun Fact")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_title)
        self.labels.append(self.label_title)

        self.label_fact = QLabel()
        self.label_fact.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_fact)
        self.labels.append(self.label_fact)
        
        # Auto-Update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_fact)
        self.timer.start(600_000)

        self.update_fact()
        
        
    def resizeEvent(self, event):  
        font_size = max(16, int(self.height() * 0.1))
        font = QFont(self.pixel_font_family, font_size)
        
        self.label_title.setFont(font)
        
        super().resizeEvent(event)
        
        
    def update_fact(self):
        fact = get_fun_fact()

        #Zeilenumbruch nach bestimmten Zeichen, aber nur an Wortgrenzen
        wrapped_fact = wrap_text(fact, 25)

        self.label_fact.setText(wrapped_fact)

        # Zeichen zählen für Fontgröße
        text_length = len(fact)
        if text_length < 80:
            size = 14
        elif text_length < 140:
            size = 12
        elif text_length < 200:
            size = 10
        elif text_length < 300:
            size = 8
        else:
            size = 7

        font = QFont(self.pixel_font_family, size)
        self.label_fact.setFont(font)



