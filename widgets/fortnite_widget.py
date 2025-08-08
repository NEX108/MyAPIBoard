# widgets/fortnite_widget.py

import requests
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QTimer
from config import API_KEY_FORTNITE
from pathlib import Path


#Spieler aus txt laden
def load_players():
    path = Path(__file__).parent / "assets" / "fortnite" / "spielernamen.txt"
    try:
        with open(path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        return [f"FEHLER: {e}"]

#API-Zugriff
def get_fortnite_stats(username):
    headers = {"Authorization": API_KEY_FORTNITE}

    try:
        # Spieler-ID abrufen
        lookup_url = "https://fortniteapi.io/v2/lookup"
        resp = requests.get(lookup_url, headers=headers, params={"username": username}, timeout=10)
        resp.raise_for_status()
        account_id = resp.json()["account_id"]

        # Statistiken abrufen
        stats_url = "https://fortniteapi.io/v1/stats"
        resp = requests.get(stats_url, headers=headers, params={"account": account_id}, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        level = data["account"]["level"]
        #minutes = data["global_stats"]["solo"].get("minutesplayed", 0)

        return f"{username}:\nLevel {level}\n" #Spielzeit: {minutes} Min."

    except Exception as e:
        return f"{username}: ❌ Fehler: {e}"

class FortniteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎮 Fortnite Stats")
        self.setMinimumWidth(300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        #Spieler laden
        self.players = load_players()
        self.labels = []
        
        #Retro
        font_path = Path(__file__).parent / "assets" / "fonts" / "PressStart2P-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.pixel_font = QFont(font_family, 12)
        
        for _ in self.players:
            label = QLabel()
            label.setFont(self.pixel_font)
            label.setWordWrap(True)
            self.layout.addWidget(label)
            self.labels.append(label)

        #Auto-Refresh
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(300_000)  # alle 5 Minuten
        self.update_data()

    def update_data(self):
        for i, username in enumerate(self.players):
            stats = get_fortnite_stats(username)
            self.labels[i].setText(stats)

