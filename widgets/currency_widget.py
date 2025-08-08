import requests
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt
from pathlib import Path


def get_exchange_rates():
    url = "https://api.frankfurter.app/latest?from=EUR&to=USD,TRY" # Währung anpassen
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["rates"]
    except Exception as e:
        return {"error": str(e)}


class CurrencyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💱 Währungsrechner")
        self.setMinimumWidth(250)
        
        #Pixel Font
        font_path = Path(__file__).parent / "assets" / "fonts" / "PressStart2P-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.pixel_font_family = font_family
        
        #Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Labels
        self.labels = []

        self.label_title = QLabel("EUR → ...")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_title)
        self.labels.append(self.label_title)

        self.label_usd = QLabel()
        self.label_usd.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_usd)
        self.labels.append(self.label_usd)

        self.label_try = QLabel()
        self.label_try.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_try)
        self.labels.append(self.label_try)

        self.update_data()
        
    
    def resizeEvent(self, event):  
        font_size = max(16, int(self.height() * 0.05))
        font = QFont(self.pixel_font_family, font_size)
        
        for lbl in self.labels:
            lbl.setFont(font)
        
        super().resizeEvent(event)
    

    def update_data(self):
        rates = get_exchange_rates()
        if "error" in rates:
            self.label_usd.setText("❌ Fehler: " + rates["error"])
            self.label_try.setText("")
            return

        usd = rates.get("USD", "–")
        tr = rates.get("TRY", "–")

        self.label_usd.setText(f"🇺🇸  USD\t{usd}")
        self.label_try.setText(f"🇹🇷  TRY\t{tr}")

