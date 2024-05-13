from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QApplication
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from DataPersistor import DataPersistor
from FileUtils import FileUtils
from datetime import datetime

class Stats(QWidget):
    updateStatsSignal = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0, 0, 800, 100)
        self.data_persistor = DataPersistor(FileUtils().getFilePath())
        self.data_loader = QThread()
        self.data_persistor.load_data_thread.moveToThread(self.data_loader)
        self.data_persistor.load_data_thread.start()
        self.data_persistor.load_data_thread.dataLoaded.connect(self.updateStatsSignal.emit)
        self.updateStatsSignal.connect(self.calculate_stats)
        self.statsLayout = QGridLayout()
        self.setLayout(self.statsLayout)

        self.statLabels = {
            "today": [QLabel("$0"), QLabel("$0"), QLabel("$0")],
            "week": [QLabel("$0"), QLabel("$0"), QLabel("$0")],
            "month": [QLabel("$0"), QLabel("$0"), QLabel("$0")],
            "allTime": [QLabel("$0"), QLabel("$0"), QLabel("$0")]
        }

        # Fügen Sie die Labels zum Layout hinzu
        for i, period in enumerate(["allTime", "today", "week", "month"], start=1):
            self.statsLayout.addWidget(self.statLabels[period][0], i, 1)
            self.statsLayout.addWidget(self.statLabels[period][1], i, 2)
            self.statsLayout.addWidget(self.statLabels[period][2], i, 3)


    def get_period(self, date):
        now = datetime.now()
        if date.date() == now.date():
            return 'today'
        elif date.isocalendar()[1] == now.isocalendar()[1]:
            return 'week'
        elif date.month == now.month:
            return 'month'
        else:
            return 'allTime'

    def calculate_stats(self, data):
        print(f"calculate_stats received data: {data}")  # Debug-Ausgabe

        stats = {
            "today": [0, 0, 0],
            "week": [0, 0, 0],
            "month": [0, 0, 0],
            "allTime": [0, 0, 0]
        }

        for item in data:
            period = self.get_period(item['timestamp'])
            print(f"period for timestamp {item['timestamp']}: {period}")  # Debug-Ausgabe
            if item['action'] == 'Einzahlung':
                stats[period][0] += item['amount']
                stats[period][1] += item['amount']
            elif item['action'] == 'Auszahlung':
                stats[period][0] -= item['amount']
                stats[period][2] += item['amount']

        for period, values in stats.items():
            self.statLabels[period][0].setText("{:,.2f}".format(values[0]).replace(",", " ").replace(".", ",").replace(" ", "."))
            self.statLabels[period][1].setText("{:,.2f}".format(values[1]).replace(",", " ").replace(".", ",").replace(" ", "."))
            self.statLabels[period][2].setText("{:,.2f}".format(values[2]).replace(",", " ").replace(".", ",").replace(" ", "."))

        self.statsLayout.update()
        self.update()
        self.repaint()
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    stats = Stats(None)
    stats.show()
    app.exec()