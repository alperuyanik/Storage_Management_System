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

x = 0
idx = 0
class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()

    def Handle_Buttons(self):
        self.refresh_button.clicked.connect(self.GET_DATA)
        self.search_button.clicked.connect(self.search)
        self.check_button.clicked.connect(self.Level)
        self.update_button.clicked.connect(self.Update)
        self.delete_button.clicked.connect(self.Delete)
        self.add_button.clicked.connect(self.Add)
        self.first_button.clicked.connect(self.First)
        self.previous_button.clicked.connect(self.Previous)
        self.next_button.clicked.connect(self.Next)
        self.last_button.clicked.connect(self.Last)
        

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

        # Displaey reference number and type number in statistics tab

        cursor2 = db.cursor()
        cursor3 = db.cursor()

        parts_number = ''' SELECT COUNT (DISTINCT PartName) from parts_table '''
        ref_number =''' SELECT COUNT (DISTINCT Reference) from parts_table '''

        result_ref_number = cursor2.execute(ref_number)
        result_part_number = cursor3.execute(parts_number)

        self.label_ref_number.setText(str(result_ref_number.fetchone()[0]))
        self.label_parts_number.setText(str(result_part_number.fetchone()[0]))

        # display & results: Min, Max number of holes in additon to their respective reference names

        cursor4 = db.cursor()
        cursor5 = db.cursor()

        min_hole = ''' SELECT MIN(NumberOfHoles), Reference from parts_table '''
        max_hole = ''' SELECT MAX(NumberOfHoles), Reference from parts_table '''

        result_min_hole = cursor4.execute(min_hole)
        result_max_hole = cursor5.execute(max_hole)

        r1 = result_min_hole.fetchone()
        r2 = result_max_hole.fetchone()

        self.label_min_hole.setText(str(r1[0]))
        self.label_max_hole.setText(str(r2[0]))
                                    
        self.label_min_hole_2.setText(str(r1[1]))
        self.label_max_hole_2.setText(str(r2[1]))

        self.First()
        self.Navigate()
        self.Next()
        self.Previous()
        self.Last()


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

    def Level(self):
        # connect to sqlite3 database add fill gui table with data.
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        command = '''SELECT Reference, PartName, Count from parts_table order by Count asc LIMIT 3 '''

        result = cursor.execute(command)
        print(result)

        self.table_2.setRowCount(0)

        for row_count, row_data in enumerate(result):
            self.table_2.insertRow(row_count)
            for column_number, data in enumerate(row_data):
                self.table_2.setItem(row_count, column_number, QTableWidgetItem(str(data)))

    def Navigate(self):
        global idx
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = ''' SELECT * from parts_table'''

        result = cursor.execute(command)

        val = result.fetchone()

        self.label_id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.number_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(int(val[8]))
    
    def Update(self):

        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        id_ = int(self.label_id.text())

        reference_=self.reference.text()
        part_name_=self.part_name.text()
        min_area_=self.min_area.text()
        max_area_=self.max_area.text()
        number_of_holes_= self.number_of_holes.text()
        min_diameter_= self.min_diameter.text()
        max_diameter_ = self.max_diameter.text()
        count_ = str(self.count.value())    # itis not string 

        row = (reference_,part_name_,min_area_,max_area_,number_of_holes_,min_diameter_,max_diameter_,count_,id_)

        command = ''' UPDATE parts_table SET Reference=?,PartName=?,MinArea=?,MaxArea=?,NumberOfHoles=?,MinDiameter=?,MaxDiameter=?,Count=? WHERE ID=? '''

        cursor.execute(command,row)

        db.commit()

    def Delete(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        d = self.label_id.text()

        command = ''' DELETE FROM parts_table WHERE ID=? '''

        cursor.execute(command,d)

        db.commit()

    def Add(self):

        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        reference_=self.reference.text()
        part_name_=self.part_name.text()
        min_area_=self.min_area.text()
        max_area_=self.max_area.text()
        number_of_holes_= self.number_of_holes.text()
        min_diameter_= self.min_diameter.text()
        max_diameter_ = self.max_diameter.text()
        count_ = str(self.count.value())    # itis not string 

        row = (reference_,part_name_,min_area_,max_area_,number_of_holes_,min_diameter_,max_diameter_,count_)

        command = ''' INSERT INTO parts_table (Reference,PartName,MinArea,MaxArea,NumberOfHoles,MinDiameter,MaxDiameter,Count) VALUES (?,?,?,?,?,?,?,?) '''

        cursor.execute(command,row)

        db.commit()

    def Next(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM parts_table '''
        result = cursor.execute(command)
        val = result.fetchall()
        tot = len(val)
        global x
        global idx

        x = x + 1

        if x<tot:
            idx = val[x][0]
            self.Navigate()
        else:
            x = x-1



    def Previous(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM parts_table '''
        result = cursor.execute(command)
        val = result.fetchall()
        tot = len(val)
        global x
        global idx

        x = x - 1

        if x>-1:
            idx = val[x][0]
            self.Navigate()
        else:
            x = 0

    def First(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM parts_table '''
        result = cursor.execute(command)
        val = result.fetchall()
        tot = len(val)
        global x
        global idx

        x = 0

        if x > -1:
            idx = val[x][0]
            self.Navigate()
        else:
            x = 0

    def Last(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM parts_table '''
        result = cursor.execute(command)
        val = result.fetchall()
        tot = len(val)
        global x
        global idx

        x = tot - 1

        if x<tot:
            idx = val[x][0]
            self.Navigate()
        else:
            x = tot-1


def main():
    app=QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()
