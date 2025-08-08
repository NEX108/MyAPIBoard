from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap
from PyQt6.QtCore import QDate, Qt
from pathlib import Path
import datetime

class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📅 Kalender")
        self.setMinimumWidth(250)
        

        # Pixel-Font laden
        font_path = Path(__file__).parent / "assets" / "fonts" / "PressStart2P-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.pixel_font_family = font_family
        
        
        #Layouts
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.content_layout = QHBoxLayout()
        self.main_layout.addLayout(self.content_layout)
        
        
        #Icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.content_layout.addWidget(self.icon_label)
        
        icon_path = Path(__file__).parent / "assets" / "calendar" / "calendar.png"
        if icon_path.exists():
            pixmap = QPixmap(str(icon_path))
            self.icon_label.setPixmap(pixmap)
            
            
        #Text Infos
        self.text_layout = QVBoxLayout()
        self.content_layout.addLayout(self.text_layout)
        
        self.label_date = QLabel()
        self.label_weekday = QLabel()
        self.label_kw = QLabel()
        
        for lbl in [self.label_date, self.label_weekday, self.label_kw]:
            lbl.setWordWrap(True)
            lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            self.text_layout.addWidget(lbl)
            
        self.update_calendar()
        

    def resizeEvent(self, event):
        icon_height = int(self.height() * 0.6)
        if self.icon_label.pixmap() and not self.icon_label.pixmap().isNull():
            pixmap = self.icon_label.pixmap()
            scaled = pixmap.scaledToHeight(icon_height, Qt.TransformationMode.SmoothTransformation)
            self.icon_label.setPixmap(scaled)
            
        font_size = max(16, int(self.height() * 0.1))
        font = QFont(self.pixel_font_family, font_size)
        
        self.label_date.setFont(font)
        self.label_weekday.setFont(font)
        self.label_kw.setFont(font)
        
        super().resizeEvent(event)


    def update_calendar(self):
        today = datetime.date.today()
        weekday = today.strftime("%A").upper()  # z. B. Sunday
        date_str = today.strftime("%d.%m.%Y")
        iso_calendar = today.isocalendar()  # Tuple: (Jahr, KW, Wochentag)

        self.label_date.setText(date_str)
        self.label_weekday.setText(f"{weekday}")
        self.label_kw.setText(f"KW {iso_calendar[1]}")

