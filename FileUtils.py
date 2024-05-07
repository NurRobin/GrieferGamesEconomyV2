from PyQt6.QtWidgets import QFileDialog, QMessageBox

import os
import sys

class FileUtils():
    def __init__(self):
        self.filepath = None
        self.getFileFromDefaultPath()

    def getFileFromDefaultPath(self):
        self.filepath = os.path.join(os.environ['APPDATA'], '.minecraft', 'labymod-neo', 'configs', 'GrieferGames', 'transactions.log')
        if self.filepath:
            return self.filepath
        else:
            self.filepath = self.askForFile()
            if self.filepath:
                return self.filepath
            else:
                sys.exit(1)

    def askForFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.Option.DontUseNativeDialog
        self.filepath, _ = QFileDialog.getOpenFileName(None, "Select transaction log file", "", "Log Files (*.log)", options=options)
        if self.filepath:
            return self.filepath
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("No file selected")
            msg.setInformativeText("You need to select a file to continue")
            msg.setWindowTitle("Error")
            msg.exec()
            return None
    
    def getFilePath(self):
        return self.filepath