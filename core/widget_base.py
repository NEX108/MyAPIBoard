# core/widget_base.py

from PyQt6.QtWidgets import QWidget
from abc import ABC, abstractmethod

class WidgetBase(QWidget, ABC):
    """Abstrakte Basisklasse für alle Widgets."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @abstractmethod
    def update_data(self):
        """Methode zum Aktualisieren der Widget-Daten (z. B. API-Aufruf)."""
        pass

    @abstractmethod
    def get_title(self) -> str:
        """Rückgabe des Widget-Titels (z. B. zur Anzeige im Dashboard)."""
        pass

