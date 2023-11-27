from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog, QPushButton,
        QTableWidget, QTableWidgetItem, QGridLayout, QDialogButtonBox, QGroupBox,
        QVBoxLayout)
import threading

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from logic.data_object import *


item = QTableWidgetItem(' ')
DEFAULT_BRUSH = item.background()
X_BRUSH = QColor(200, 200, 255)
Y_BRUSH = QColor(255, 200, 200)

def group_box_factory(group_name, *buttons):
    groupBox = QGroupBox(group_name)
    layout = QVBoxLayout()
    for button in buttons:
        layout.addWidget(button)
    groupBox.setLayout(layout)
    return groupBox

class DataHandler(QDialog):
    def __init__(self, data_obj: DataObject = None, parent = None):
        super().__init__(parent)
        self.data_obj = data_obj

        self.setWindowTitle("Data Handler")
        self.resize(1200, 1000)

        self.createTable()
        self.createButtons()
        self.layout()


    def createTable(self):
        if self.data_obj is None:
            self.tableWidget = QTableWidget(20, 10)
            return
        n_rows, n_cols = self.data_obj.shape()
        self.tableWidget = QTableWidget(n_rows, n_cols)
        self.tableWidget.setHorizontalHeaderLabels(self.data_obj.columns())

        for row in range(n_rows):
            for col in range(n_cols):
                item = QTableWidgetItem(str(self.data_obj.iloc(row, col)))
                if col == self.data_obj.X: item.setBackground(X_BRUSH)
                if col == self.data_obj.Y: item.setBackground(Y_BRUSH)
                self.tableWidget.setItem(row, col, item)


    def updateTable(self):
        n_rows, n_cols = self.data_obj.shape()
        for row in range(n_rows):
            for col in range(n_cols):
                item = QTableWidgetItem(str(self.data_obj.iloc(row, col)))
                if col == self.data_obj.X: item.setBackground(X_BRUSH)
                if col == self.data_obj.Y: item.setBackground(Y_BRUSH)
                self.tableWidget.setItem(row, col, item)
    

    def updateTableColor(self):
        n_rows, n_cols = self.data_obj.shape()
        for col in range(n_cols):
            if col == self.data_obj.X: use_brush = X_BRUSH
            elif col == self.data_obj.Y: use_brush = Y_BRUSH
            else: use_brush = DEFAULT_BRUSH

            for row in range(n_rows):
                item = self.tableWidget.item(row, col)
                item.setBackground(use_brush)

    
    def createButtons(self):
        self.selectXButton = QPushButton("Select X")
        self.selectXButton.clicked.connect(self.selectX)

        self.selectYButton = QPushButton("Select Y")
        self.selectYButton.clicked.connect(self.selectY)

        self.dropRowButton = QPushButton("Delete row")
        self.dropRowButton.clicked.connect(self.dropRow)

        self.dropColButton = QPushButton("Delete column")
        self.dropColButton.clicked.connect(self.dropCol)


    def layout(self):
        group_xy = group_box_factory("Set X-Y", self.selectXButton, self.selectYButton)
        group_cleaning = group_box_factory("Data Cleaning", self.dropRowButton, self.dropColButton)

        control_layout = QVBoxLayout()
        control_layout.addWidget(group_xy)
        control_layout.addWidget(group_cleaning)

        layout = QGridLayout()
        layout.addLayout(control_layout, 0, 2, 4, 2)

        self.tableWidget.setMinimumWidth(500)
        layout.addWidget(self.tableWidget, 0, 0, 4, 1)
        

        self.setLayout(layout)


    def selectX(self):
        def setX():
            n_rows, n_cols = self.data_obj.shape()
            for row in range(n_rows):
                for col in range(n_cols):
                    if self.tableWidget.item(row, col).isSelected():
                        self.data_obj.setX(col)
                        return
        setX()
        self.updateTableColor()
                

    def selectY(self):
        def setY():
            n_rows, n_cols = self.data_obj.shape()
            for row in range(n_rows):
                for col in range(n_cols):
                    if self.tableWidget.item(row, col).isSelected():
                        self.data_obj.setY(col)
                        return
        setY()
        self.updateTableColor()


    def dropRow(self):
        def dropSelectedRow():
            indices = []
            n_rows, n_cols = self.data_obj.shape()
            for row in range(n_rows):
                for col in range(n_cols):
                    if self.tableWidget.item(row, col).isSelected():
                        indices.append(row)
                        break
            self.data_obj.drop_row(indices)
            for _ in range(len(indices)):
                self.tableWidget.removeRow(0)

        with threading.Lock():
            dropSelectedRow()
            self.updateTable()


    def dropCol(self):
        def dropSelectedCol():
            indices = []
            n_rows, n_cols = self.data_obj.shape()
            for row in range(n_rows):
                for col in range(n_cols):
                    if col in indices: continue
                    if self.tableWidget.item(row, col).isSelected():
                        indices.append(col)
            self.data_obj.drop_col(indices)
            for _ in range(len(indices)):
                self.tableWidget.removeColumn(0)
            self.tableWidget.setHorizontalHeaderLabels(self.data_obj.columns())

        with threading.Lock():
            dropSelectedCol()
            self.updateTable()


if __name__ == '__main__':
    do = read_csv("weather.csv")

    app = QApplication([])
    data_handler = DataHandler(do)
    data_handler.show()
    app.exec()
