from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

import sys

from os import path

from PyQt5.uic import loadUiType

import os

current_directory = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(current_directory, "main.ui")

FORM_CLASS,_ = loadUiType(ui_path)

import sqlite3


class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()

    def Handle_Buttons(self):
        self.refresh_button.clicked.connect(self.GET_DATA)
        self.search_button.clicked.connect(self.search)

    def GET_DATA(self):
        # connect to sqlite3 database add fill gui table with data.
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        command = '''SELECT * from parts_table'''

        result = cursor.execute(command)
        print(result)

        self.table.setRowCount(0)

        for row_count, row_data in enumerate(result):
            self.table.insertRow(row_count)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_count, column_number, QTableWidgetItem(str(data)))

        cursor2 = db.cursor()
        cursor3 = db.cursor()

        parts_number = ''' SELECT COUNT (DISTINCT PartName) from parts_table '''
        ref_number =''' SELECT COUNT (DISTINCT Reference) from parts_table '''

        result_ref_number = cursor2.execute(ref_number)
        result_part_number = cursor3.execute(parts_number)

        self.label_ref_number.setText(str(result_ref_number.fetchone()[0]))
        self.label_parts_number.setText(str(result_part_number.fetchone()[0]))

    def search(self):
        db = sqlite3.connect("storage_management_env/parts.db")
        cursor = db.cursor()
        
        command = ''' SELECT * from parts_table WHERE count<=? '''

        my_number = int(self.count_filter_txt.text())

        result = cursor.execute(command,[my_number])

        self.table.setRowCount(0)

        for row_count, row_data in enumerate(result):
            self.table.insertRow(row_count)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_count, column_number, QTableWidgetItem(str(data)))


    # Here is our code

def main():
    app=QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()
