# main.py

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QSizePolicy
)
from widgets.weather_widget import WeatherWidget
from widgets.bitcoin_widget import BitcoinWidget
from widgets.vgn_widget import VGNWidget
from widgets.clock_widget import ClockWidget
from widgets.fortnite_widget import FortniteWidget
from widgets.calendar_widget import CalendarWidget
from widgets.nasa_widget import NasaWidget
from widgets.funfact_widget import FunFactWidget
from widgets.currency_widget import CurrencyWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MyAPIBoard")
        self.setMinimumSize(900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(8, 8, 8, 8)
        self.grid_layout.setSpacing(8)
        central_widget.setLayout(self.grid_layout)

        # Alle Spalten und Zeilen gleich gewichten
        for i in range(3):
            self.grid_layout.setColumnStretch(i, 1)
            self.grid_layout.setRowStretch(i, 1)

        # Funktion zum Standard-SizePolicy
        def standard_widget(widget):
            widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
            return widget

        # Widgets erstellen
        weather = standard_widget(WeatherWidget())
        bitcoin = standard_widget(BitcoinWidget())
        vgn = standard_widget(VGNWidget())
        clock = standard_widget(ClockWidget())
        fortnite = standard_widget(FortniteWidget())
        calendar = standard_widget(CalendarWidget())
        nasa = standard_widget(NasaWidget())
        funfact = standard_widget(FunFactWidget())
        currency = standard_widget(CurrencyWidget())

        # Widgets im Grid platzieren (3x3 gleichmäßig)
        self.grid_layout.addWidget(weather,   0, 0)
        self.grid_layout.addWidget(nasa,      0, 1)
        self.grid_layout.addWidget(vgn,       0, 2)

        self.grid_layout.addWidget(clock,     1, 0)
        self.grid_layout.addWidget(fortnite,  1, 1)
        self.grid_layout.addWidget(calendar,  1, 2)

        self.grid_layout.addWidget(bitcoin,   2, 0)
        self.grid_layout.addWidget(funfact,   2, 1)
        self.grid_layout.addWidget(currency,  2, 2)
        
    def resizeEvent(self, event):
        #verfügbaare Fläche
        cw = self.centralWidget()
        w = max(1, cw.width())
        h = max(1, cw.height())
        
        spacing = self.grid_layout.spacing()
        # 2 Lücken zwischen 3 Zeilen/Spalten
        per_col = (w-2*spacing)//3
        per_row = (h-2*spacing)//3
        
        for i in range(3):
            self.grid_layout.setColumnMinimumWidth(i, per_col)
            self.grid_layout.setRowMinimumHeight(i, per_row)
            
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Schwarzer Hintergrund mit weißer Schrift
    app.setStyleSheet("""
        QWidget {
            background-color: black;
            color: white;
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

