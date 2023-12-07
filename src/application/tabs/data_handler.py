from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QWidget, QCheckBox,
        QTableWidget, QTableWidgetItem, QGridLayout, QGroupBox,
        QVBoxLayout, QLineEdit)
import threading

from application.tabs.plot_data_handler import *
from logic.data_object import *
from logic.plot_data import *
from util.app_util import *
from util import cleaning


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
        self.clean_btn = btn_factory("Drop if", self.dropif)
        self.reset_btn = btn_factory("Reset data", self.reset)
        self.condition_entry = QLineEdit()
        self.cln_selected_col_checkbox = QCheckBox("Only clean selected columns")
        self.cln_selected_col_checkbox.setChecked(True)


    def layout(self):
        group_list = []
        group_list.append(group_box_factory("Set X-Y", self.select_X_btn, self.select_Y_btn))
        group_list.append(group_box_factory("Table Adjustment", self.drop_row_btn, self.drop_col_btn))

        cleaning_layout = couple_layout(self.clean_btn, self.condition_entry)
        group_list.append(group_box_factory("Data Cleaning", self.cln_selected_col_checkbox, cleaning_layout))

        control_layout = QVBoxLayout()
        control_layout.addStretch()
        for group in group_list:
            control_layout.addWidget(group)
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
            indices = get_selected_columns(self.tableWidget)
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
    def dropif(self):
        command = self.condition_entry.text()
        if self.cln_selected_col_checkbox.isChecked():
            selected_cols = get_selected_columns(self.tableWidget)
        else:
            _, n_cols = self.data_obj.shape()
            selected_cols = range(n_cols)
        self.data_obj.dropif(cleaning.clean(command, selected_cols))
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
