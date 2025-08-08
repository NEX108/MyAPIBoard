import requests
import random
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

API_BASE = "https://anime-facts-rest-api.herokuapp.com/api/v1"

def fetch_anime_list():
    try:
        resp = requests.get(API_BASE, timeout=10)
        resp.raise_for_status()
        return [entry["anime_name"] for entry in resp.json().get("data", [])]
    except Exception:
        return []

def fetch_fact(anime_name):
    try:
        resp = requests.get(f"{API_BASE}/{anime_name}", timeout=10)
        resp.raise_for_status()
        facts = resp.json().get("data", [])
        if facts:
            choice = random.choice(facts)
            return choice.get("fact", "Kein Fakt gefunden.")
        return "Keine Fakten verfügbar."
    except Exception as e:
        return f"❌ Fehler: {e}"

class AnimeFactsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 Anime-Fakt des Tages")
        self.setMinimumWidth(300)

        self.layout = QVBoxLayout()
        self.label_fact = QLabel("Lade Anime-Fakt …")
        self.label_fact.setWordWrap(True)
        self.label_fact.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_fact.setFont(QFont("Arial", 11))

        self.setLayout(self.layout)
        self.layout.addWidget(self.label_fact)

        self.update_fact()

    def update_fact(self):
        anime_list = fetch_anime_list()
        if not anime_list:
            self.label_fact.setText("❌ Keine Anime-Liste gefunden.")
            return
        random_anime = random.choice(anime_list)
        fact = fetch_fact(random_anime)
        self.label_fact.setText(f"🗒️ [{random_anime.replace('_', ' ').title()}]\n{fact}")

