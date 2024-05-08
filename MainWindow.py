from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QFileDialog, QMessageBox, QStatusBar, QLabel
from PyQt6.QtGui import QIcon, QPixmap

import Toolbar
import List
import Stats
from Utils import getAppIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Griefer Games Transaction Viewer v2.0")
        # Add Icon
        self.setWindowIcon(QIcon(getAppIcon()))
        # self.setStyleSheet("""
        #             QWidget {
        #                 font-family: 'Segoe UI';
        #                 font-size: 10pt;
        #             }
        #             QPushButton {
        #                 background-color: #0078D7;
        #                 color: white;
        #                 border-radius: 5px;
        #                 padding: 5px;
        #             }
        #             QPushButton:hover {
        #                 background-color: #005EA6;
        #             }
        #             QListWidget {
        #                 border: 1px solid #D3D3D3;
        #             }
        #             QListWidget::item {
        #                 text-align: left;
        #                 margin: 2px; /* Kleiner Abstand zwischen den Einträgen */
        #                 padding: 2px; /* Innenabstand für jeden Eintrag */
        #                 min-height: 30px; /* Minimale Höhe jedes Eintrags */
        #                 line-height: 30px; /* Stellt den Text vertikal zentriert ein */
        #             }
        #             QListWidget::item:selected {
        #                 background-color: #0078D7;
        #                 color: white;
        #             }
        #             QLabel {
        #                 color: #EEEEEE;
        #             }
        #         """)
        self.resize(800, 600)
        #List
        self.list = List.List(self)
        #Toolbar
        self.toolbar = Toolbar.Toolbar(self, self.list)
        self.setMenuBar(self.toolbar)
        # Set the list as the central widget
        self.setCentralWidget(self.list)
        #Stats
        self.stats = Stats.Stats(self)
        # Create a QStatusBar instance
        self.status_bar = QStatusBar()
        # Add your Stats widget to the status bar
        self.status_bar.addWidget(self.stats)
        # Set the status bar
        self.setStatusBar(self.status_bar)
        #Show
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()