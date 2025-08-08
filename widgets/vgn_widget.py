# widgets/vgn_widget.py

import requests
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QTimer
from datetime import datetime, timezone
from pathlib import Path
import dateutil.parser

# =========================
# 🔧 SCHNELL-EINSTELLUNGEN
# =========================

# Verkehrsunternehmen (laut API-Pfad)
AGENCY = "VAG"

# Haltestellen-Kennung aus der API (z.B. "FR" = Frankenstraße)
STOP_ID = "FR"

# Eigene Header-Texte je Haltepunkt (optional).
# Wenn None, wird automatisch der erste "Richtungstext" aus der API pro Haltepunkt genommen.
# FR:1 (stadtauswärts), FR:2 (stadteinwärts) – je nach Station kann das variieren.
"""
CUSTOM_HEADERS = {
    "FR:1": "FÜRTH HARDHÖHE / EBERHARDSHOF",
    "FR:2": "LANGWASSER SÜD",
}
"""
CUSTOM_HEADERS = None

# Wie viele Abfahrten je Haltepunkt anzeigen?
MAX_PER_TRACK = 3

# Nur Abfahrten in den nächsten X Minuten
TIME_WINDOW_MIN = 60

# Optional: nur bestimmte Linien zeigen (z.B. nur U1). Leerlassen = alle.
LINE_FILTER = {"U1"}  # oder: set() für keine Filterung

# Pixel-Font (relativ zum Widget)
PIXEL_FONT_PATH = Path(__file__).parent / "assets" / "fonts" / "PressStart2P-Regular.ttf"

# =========================
# Ende Schnell-Einstellungen
# =========================


def _build_url(agency: str, stop_id: str) -> str:
    return f"https://start.vag.de/dm/api/v1/abfahrten/{agency}/{stop_id}"


def get_departures():
    """Liest Abfahrten und gruppiert sie nach Haltepunkt (z.B. FR:1 / FR:2)."""
    try:
        url = _build_url(AGENCY, STOP_ID)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        now = datetime.now(timezone.utc)

        grouped = {}
        for entry in data.get("Abfahrten", []):
            line = entry.get("Linienname", "")
            if LINE_FILTER and line not in LINE_FILTER:
                continue

            haltepunkt = entry.get("Haltepunkt", "")
            richtung_text = entry.get("Richtungstext", "").upper()
            ts = entry.get("AbfahrtszeitIst") or entry.get("AbfahrtszeitSoll")
            if not ts:
                continue

            try:
                t = dateutil.parser.parse(ts)
            except Exception:
                continue

            minutes = int((t - now).total_seconds() / 60)
            if minutes < 0 or minutes > TIME_WINDOW_MIN:
                continue

            row = f"{line:<3} → {richtung_text:<18}  {minutes:>2} MIN"

            if haltepunkt not in grouped:
                grouped[haltepunkt] = {
                    "header": richtung_text,   # Fallback, kann später durch CUSTOM_HEADERS ersetzt werden
                    "rows": []
                }

            if len(grouped[haltepunkt]["rows"]) < MAX_PER_TRACK:
                grouped[haltepunkt]["rows"].append(row)

        # Header ggf. überschreiben
        if CUSTOM_HEADERS:
            for key, header in CUSTOM_HEADERS.items():
                if key in grouped:
                    grouped[key]["header"] = header

        return grouped

    except Exception as e:
        return {"FEHLER": str(e)}


class VGNWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚇 VGN Abfahrten")

        # Pixel-Font laden
        font_id = QFontDatabase.addApplicationFont(str(PIXEL_FONT_PATH))
        families = QFontDatabase.applicationFontFamilies(font_id)
        family = families[0] if families else "Monospace"
        self._base_family = family

        # Hauptlayout
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        self.setLayout(layout)

        # Drei Labels: FR:1, FR:2, Fehler
        self.labels = {
            "FR:1": QLabel(),
            "FR:2": QLabel(),
            "FEHLER": QLabel()
        }

        for lbl in self.labels.values():
            lbl.setWordWrap(True)
            # WICHTIG: nicht die Zeilenhöhe hochtreiben
            lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
            layout.addWidget(lbl)

        # Erstes Styling
        self._apply_font_by_height()

        # Auto-Update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(20_000)  # alle 20 Sekunden
        self.update_data()

    def _apply_font_by_height(self):
        # Dynamische Schriftgröße anhand Widget-Höhe
        h = max(1, self.height())
        px = max(6, h // 25)
        font = QFont(self._base_family, px)
        for lbl in self.labels.values():
            lbl.setFont(font)

    def resizeEvent(self, event):
        self._apply_font_by_height()
        super().resizeEvent(event)

    def update_data(self):
        data = get_departures()

        # Fehlerbehandlung
        if "FEHLER" in data:
            self.labels["FEHLER"].setText(f"❌ FEHLER: {data['FEHLER'].upper()}")
            self.labels["FR:1"].setText("")
            self.labels["FR:2"].setText("")
            return
        else:
            self.labels["FEHLER"].setText("")

        # Anzeigen in fixer Reihenfolge
        for key in ("FR:1", "FR:2"):
            if key in data:
                header = data[key]["header"]
                rows = data[key]["rows"]
                # Extra Zeilenabstand via doppelte \n
                self.labels[key].setText(f"{header}\n\n" + "\n\n".join(rows))
            else:
                self.labels[key].setText("")

