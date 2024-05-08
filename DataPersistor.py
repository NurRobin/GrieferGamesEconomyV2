# DataPersistor.py
from PyQt6.QtCore import QFileSystemWatcher, QThread, pyqtSignal
from Utils import parse_line, ConvertToEuro
from FileUtils import FileUtils

class LoadDataThread(QThread):
    dataLoaded = pyqtSignal(list)

    def __init__(self, file_path):
        QThread.__init__(self)
        self.file_path = file_path

    def run(self):
        data = []
        with open(self.file_path, 'r') as file:
            for line in file:
                data_line = parse_line(line)
                irl_amount = ConvertToEuro(data_line['amount'])
                data_line['formatted_amount'] = "{:,.2f}".format(float(data_line['amount'])).replace(",", " ").replace(".", ",").replace(" ", ".")
                data_line['formatted_irlAmount'] = "{:,.2f}".format(irl_amount).replace(",", " ").replace(".", ",").replace(" ", ".")
                data_line['timestamp_label'] = data_line['timestamp'].strftime("%d.%m.%Y %H:%M:%S")
                data_line['player'] = data_line['player'].replace("\n", "")
                data.append(data_line)
        data = sorted(data, key=lambda x: x['timestamp'], reverse=True)
        self.dataLoaded.emit(data)

class DataPersistor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.load_data_thread = LoadDataThread(self.file_path)
        self.load_data_thread.dataLoaded.connect(self.on_data_loaded)
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.addPath(FileUtils().getFilePath())
        self.file_watcher.fileChanged.connect(self.trigger_reload)

    def trigger_reload(self):
        self.load_data_thread.start()

    def on_data_loaded(self, data):
        self.data = data

    def get_data(self):
        return self.data