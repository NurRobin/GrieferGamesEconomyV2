from PyQt6.QtCore import QFileSystemWatcher, QThread
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QListWidget, QListWidgetItem, QLabel, QCheckBox, QInputDialog, QMessageBox, QGridLayout, QLineEdit

from FileUtils import FileUtils
from DataPersistor import DataPersistor
from Utils import parse_line, ConvertToEuro

class List(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.isPaused = False
        self.data_persistor = DataPersistor(FileUtils().getFilePath())
        self.data_loader = QThread()
        self.data_persistor.load_data_thread.moveToThread(self.data_loader)
        self.data_persistor.load_data_thread.start()
        self.data_persistor.load_data_thread.dataLoaded.connect(self.add_items_to_list)
        self.data_loader.started.connect(self.data_persistor.load_data_thread.run)
        self.data_loader.finished.connect(self.data_loader.deleteLater)
        layout = QVBoxLayout()
        self.listWidget = QListWidget()
        layout.addWidget(self.listWidget)
        self.setLayout(layout)  # Set the layout to the widget
        self.listWidget.setSortingEnabled(False)  # We will sort manually
        self.listWidget.setWordWrap(True)
        self.file_utils = FileUtils()
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.addPath(self.file_utils.getFilePath())
        self.file_watcher.fileChanged.connect(self.refresh)

        self.load_data()

    def load_data(self):
        self.data_persistor.trigger_reload()

    def refresh(self, trigger="Auto Reload"):
        if self.isPaused and trigger == "Auto Reload":
            return
        self.listWidget.clear()  # Clear the listWidget
        self.data_loader.start()  # Start the data loader thread
    
    def add_items_to_list(self, data):
        for item in data:
            self.add_item_to_list(item)

    def add_item_to_list(self, data):
        print(data)
        item = QListWidgetItem()
        widget = QWidget()
        layout = QHBoxLayout()
        
        irlAmount = ConvertToEuro(data['amount'])
        
        # Format amount and irlAmount with dots as thousand separators and comma as decimal separator
        formatted_amount = "{:,.2f}".format(float(data['amount'])).replace(",", " ").replace(".", ",").replace(" ", ".")
        formatted_irlAmount = "{:,.2f}".format(irlAmount).replace(",", " ").replace(".", ",").replace(" ", ".")
        
        timestamp_label = QLabel(data['timestamp'].strftime("%d.%m.%Y %H:%M:%S"))
        action_label = QLabel(data['action'])
        amount_label = QLabel(formatted_amount)  # Use formatted amount
        irlAmount_label = QLabel(formatted_irlAmount)  # Use formatted irlAmount
        player_label = QLabel(data['player'])
        
        layout.addWidget(timestamp_label)
        layout.addWidget(action_label)
        layout.addWidget(amount_label)
        layout.addWidget(irlAmount_label)
        layout.addWidget(player_label)
        
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        
        item.setSizeHint(widget.sizeHint())
        
        self.listWidget.addItem(item)  # Add item to the listWidget
        self.listWidget.setItemWidget(item, widget)  # Set the widget to the item
        
if __name__ == "__main__":
    app = QApplication([])
    window = List(None)
    window.show()
    app.exec()