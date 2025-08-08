import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QTimer, Qt
from datetime import datetime
from pathlib import Path
import pytz


class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🕰️ Retro Clock")
        self.setMinimumWidth(300)
        
        #Pixel Font
        font_path = Path(__file__).parent / "assets" / "fonts" / "PressStart2P-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.pixel_font_family = font_family
        
        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        #Labels
        self.labels = []

        self.label_nbg = QLabel()
        self.label_nbg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_nbg)
        self.labels.append(self.label_nbg)

        self.label_ist = QLabel()
        self.label_ist.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_ist)
        self.labels.append(self.label_ist)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(500)

        self.update_time()
        
        
    def resizeEvent(self, event):  
        font_size = max(16, int(self.height() * 0.1))
        font = QFont(self.pixel_font_family, font_size)
        
        for lbl in self.labels:
            lbl.setFont(font)
        
        super().resizeEvent(event)
        

    def update_time(self):
        tz_nbg = pytz.timezone("Europe/Berlin")
        tz_ist = pytz.timezone("Europe/Istanbul")

        now_nbg = datetime.now(tz_nbg).strftime("%H:%M:%S")
        now_ist = datetime.now(tz_ist).strftime("%H:%M:%S")

        self.label_nbg.setText("Nürnberg"+"\n"+f"{now_nbg}")
        self.label_ist.setText("Istanbul"+"\n"+f"{now_ist}")

