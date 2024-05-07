from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction

import Export
from List import List

# Toolbar for the Main Window

class Toolbar(QMenuBar):
    def __init__(self, parent, list_instance):
        super().__init__(parent)
        self.list_instance = list_instance

        # Export Menu
        exportMenu = self.addMenu("Export")
        exportMenu.addAction("CSV Export").triggered.connect(Export.export_to_csv)
        exportMenu.addAction("JSON Export")

        # Refresh Menu
        refreshMenu = self.addMenu("Refresh")
        refreshMenu.addAction("Manuell Neuladen").triggered.connect(self.manual_reload)
        # Add Checkable Action
        action = refreshMenu.addAction("Auto Neuladen")
        action.setCheckable(True)
        action.setChecked(True)
        action.triggered.connect(self.auto_reload)

    def manual_reload(self):
        self.list_instance.refresh("Manuell Neuladen")
        
    def auto_reload(self, action):
        if action:
            self.list_instance.isPaused = False
            self.list_instance.refresh("Auto Reload")
        else:
            self.list_instance.isPaused = True