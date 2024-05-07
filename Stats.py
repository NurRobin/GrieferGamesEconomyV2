from PyQt6 import QtWidgets

class Stats(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0, 0, 800, 100)
        self.setStyleSheet("background-color: lightgray")
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QtWidgets.QLabel("Stats"))
        self.layout.addWidget(QtWidgets.QLabel("Total: 0"))
        self.layout.addWidget(QtWidgets.QLabel("Average: 0"))
        self.layout.addWidget(QtWidgets.QLabel("Max: 0"))
        self.layout.addWidget(QtWidgets.QLabel("Min: 0"))
                              
    def refresh(self):
        print("Refresh")
        # Calculate Stats
        # Update Labels
        pass