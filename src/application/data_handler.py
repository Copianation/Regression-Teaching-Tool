from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
        QTableWidget, QTableWidgetItem, QGridLayout, QGroupBox,
        QVBoxLayout)
import threading

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from application.plot_data_handler import *
from logic.data_object import *
from logic.plot_data import *
from util.app_util import *


item = QTableWidgetItem(' ')
DEFAULT_BRUSH = item.background()
X_BRUSH = QColor(200, 200, 255)
Y_BRUSH = QColor(255, 200, 200)


def update_plot_data(func):
    def wrapper(self):
        func(self)
        self.plt_data.retrieve_plt_df()
        self.plt_d_handler.updateTableContent()
    return wrapper



class DataHandler(QWidget):
    def __init__(self, data_obj: DataObject, plt_data: PlotData, plt_d_handler: PltDataHandler, parent = None):
        super().__init__(parent)
        self.data_obj = data_obj
        self.plt_data = plt_data
        self.plt_d_handler = plt_d_handler

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

        self.updateTableContent()


    def updateTableContent(self):
        self.tableWidget.setHorizontalHeaderLabels(self.data_obj.columns())
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
        self.select_X_btn = btn_factory("Select X", self.selectX)
        self.select_Y_btn = btn_factory("Select Y", self.selectY)
        self.drop_row_btn = btn_factory("Delete row", self.dropRow)
        self.drop_col_btn = btn_factory("Delete column", self.dropCol)
        self.dropna_btn = btn_factory("Drop Na", self.dropna)
        self.reset_btn = btn_factory("Reset data", self.reset)


    def layout(self):
        group_xy = group_box_factory("Set X-Y", self.select_X_btn, self.select_Y_btn)
        group_cleaning = group_box_factory("Data Cleaning", self.drop_row_btn, self.drop_col_btn, self.dropna_btn)

        control_layout = QVBoxLayout()
        control_layout.addStretch()
        control_layout.addWidget(group_xy)
        control_layout.addWidget(group_cleaning)
        control_layout.addWidget(self.reset_btn)

        layout = QGridLayout()
        layout.addLayout(control_layout, 0, 2, 4, 2)

        self.tableWidget.setMinimumWidth(400)
        layout.addWidget(self.tableWidget, 0, 0, 4, 1)

        self.setLayout(layout)

    @update_plot_data
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
                
    @update_plot_data
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

    @update_plot_data
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
            self.updateTableContent()

    @update_plot_data
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
            self.updateTableContent()

    @update_plot_data
    def dropna(self):
        self.data_obj.dropna()
        self.tableWidget.setRowCount(self.data_obj.shape()[0])
        self.updateTableContent()

    def reset(self):
        self.data_obj.reset()
        n_rows, n_cols = self.data_obj.shape()
        self.tableWidget.setRowCount(n_rows)
        self.tableWidget.setColumnCount(n_cols)
        self.tableWidget.setHorizontalHeaderLabels(self.data_obj.columns())
        self.updateTableContent()



if __name__ == '__main__':
    do = read_csv("titanic.csv")

    app = QApplication([])
    data_handler = DataHandler(do)
    data_handler.show()
    app.exec()
