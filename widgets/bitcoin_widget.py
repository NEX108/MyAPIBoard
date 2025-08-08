from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QApplication
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer, QSize
from pathlib import Path
from config import API_KEY_FINANCE
import sys
import requests


# 🔐 API-Zugriff
def get_bitcoin_data():
    try:
        res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true", timeout=10)
        res.raise_for_status()
        data = res.json()["bitcoin"]
        return {
            "price": round(data["usd"], 2),
            "change": round(data["usd_24h_change"], 2)
        }
    except Exception as e:
        return {"error": str(e)}

def get_shell_data():
    try:
        url = f"https://financialmodelingprep.com/api/v3/quote/R6C0.F?apikey={API_KEY_FINANCE}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()[0]
        
        #Falls API nichts zurückgibt
        if not data or not insinstance(data, list):
            return {"error": "Keine Daten von API"}
            
        stock = data[0]
        
        return {
            "price": round(data["price"], 2),
            "change": round(data["changesPercentage"], 2)
        }
    except Exception as e:
        return {"error": str(e)}

class BitcoinWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 📦 Pixel-Font laden
        font_id = QFontDatabase.addApplicationFont("/home/nex108/myapiboard/widgets/assets/fonts/PressStart2P-Regular.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.pixel_font_family = font_family

        self.setMinimumSize(300, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # --- BTC ICON & TEXT ---
        self.btc_icon = QLabel()
        self.btc_icon.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.btc_movie = None
        self.btc_text = QLabel()
        self.btc_text.setWordWrap(True)

        btc_layout = QHBoxLayout()
        btc_layout.addWidget(self.btc_icon)
        btc_layout.addWidget(self.btc_text)
        self.layout.addLayout(btc_layout)

        # --- SHELL ICON & TEXT ---
        self.shell_icon = QLabel()
        self.shell_icon.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.shell_text = QLabel()
        self.shell_text.setWordWrap(True)

        shell_layout = QHBoxLayout()
        shell_layout.addWidget(self.shell_icon)
        shell_layout.addWidget(self.shell_text)
        self.layout.addLayout(shell_layout)

        # 🔁 Auto-Update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(300_000)

        self.update_data()

    def update_data(self):
        widget_height = self.height()
        font_size = max(6, widget_height // 20)
        font = QFont(self.pixel_font_family, font_size)
        self.btc_text.setFont(font)
        self.shell_text.setFont(font)

        # --- Bitcoin GIF ---
        gif_path = Path(__file__).parent / "assets" / "bitcoin" / "bitcoin.gif"
        if gif_path.exists():
            self.btc_movie = QMovie(str(gif_path))
            self.btc_movie.setScaledSize(QSize(widget_height // 3, widget_height // 3))
            self.btc_icon.setMovie(self.btc_movie)
            self.btc_movie.start()
        else:
            self.btc_icon.setText("❌")

        # --- BTC Daten ---
        btc = get_bitcoin_data()
        if "error" in btc:
            self.btc_text.setText("❌ FEHLER")
        else:
            color = "green" if btc["change"] >= 0 else "red"
            arrow = "📈" if btc["change"] >= 0 else "📉"
            formatted_price = f"{int(btc['price']):,}".replace(",", ".")
            self.btc_text.setText(
                f"{formatted_price}$<br>"
                f"<span style='color:{color};'>{btc['change']}%{arrow}</span>"
            )

        # --- Shell ICON ---
        shell_icon_path = Path(__file__).parent / "assets" / "bitcoin" / "shell.png"
        if shell_icon_path.exists():
            pixmap = QPixmap(str(shell_icon_path)).scaledToHeight(widget_height // 3, Qt.TransformationMode.SmoothTransformation)
            self.shell_icon.setPixmap(pixmap)
        else:
            self.shell_icon.setText("❌")

        # --- Shell Daten ---
        shell = get_shell_data()
        if "error" in shell:
            self.shell_text.setText("❌ FEHLER")
        else:
            color = "green" if shell["change"] >= 0 else "red"
            arrow = "📈" if shell["change"] >= 0 else "📉"
            self.shell_text.setText(
                f"{shell['price']} €<br>"
                f"<span style='color:{color};'>{shell['change']}% {arrow}</span>"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BitcoinWidget()
    window.show()
    sys.exit(app.exec())

