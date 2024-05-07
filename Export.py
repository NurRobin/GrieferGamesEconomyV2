from PyQt6.QtWidgets import QFileDialog, QMessageBox
import csv

import FileUtils
import Utils

def export_to_csv():
    print("Trying to export to CSV")
    file = FileUtils.FileUtils().getFilePath()
    fileName, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()", "","CSV Files (*.csv)", options=QFileDialog.Option.DontUseNativeDialog)
    if fileName:
        with open(file, mode='r') as log, open(fileName, mode='w', newline='') as csv_file:
            fieldnames = ['timestamp', 'action', 'amount', 'player']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for line in log:
                data = Utils.parse_line(line)
                if data is None:
                    continue
                # Convert amount to negative if action is 'Payed'
                if data['action'].lower() == 'payed':
                    data['amount'] = -float(data['amount'])
                writer.writerow(data)