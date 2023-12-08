from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit,
        QTableWidget, QTableWidgetItem, QGridLayout, QGroupBox, QCheckBox,
        QVBoxLayout)
import threading

from logic.plot_data import *
from util.app_util import *
from util import cleaning


item = QTableWidgetItem(' ')
DEFAULT_BRUSH = item.background()
X_BRUSH = QColor(200, 200, 255)
Y_BRUSH = QColor(255, 200, 200)


class PltDataHandler(QWidget):
    def __init__(self, plt_data: PlotData = None, parent = None):
        super().__init__(parent)
        self.plt_data = plt_data

        self.setWindowTitle("Data Handler")

        self.createTable()
        self.createButtons()
        self.layout()


    def createTable(self):
        if self.plt_data is None:
            self.tableWidget = QTableWidget(20, 10)
            return
        n_rows, n_cols = self.plt_data.shape()
        self.tableWidget = QTableWidget(n_rows, n_cols)

        self.updateTableContent()


    def updateTableContent(self):
        header = ["Y: " + self.plt_data.columns()[0], "X: " + self.plt_data.columns()[1]]
        self.tableWidget.setHorizontalHeaderLabels(header)
        n_rows, n_cols = self.plt_data.shape()
        self.tableWidget.setRowCount(n_rows)
        for row in range(n_rows):
            for col in range(n_cols):
                item = QTableWidgetItem(str(self.plt_data.iloc(row, col)))
                if col == 1: item.setBackground(X_BRUSH)
                if col == 0: item.setBackground(Y_BRUSH)
                self.tableWidget.setItem(row, col, item)

    
    def createButtons(self):
        self.drop_row_btn = btn_factory("Delete row", self.dropRow)
        self.clean_btn = btn_factory("Drop if", self.dropif)
        self.reset_btn = btn_factory("Reset data", self.reset)
        self.condition_entry = QLineEdit()
        self.cln_selected_col_checkbox = QCheckBox("Only clean selected columns")
        self.cln_selected_col_checkbox.setChecked(True)


    def layout(self):
        group_list = []
        group_list.append(group_box_factory("Table Adjustment", self.drop_row_btn))

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


    def dropRow(self):
        def dropSelectedRow():
            indices = []
            n_rows, n_cols = self.plt_data.shape()
            for row in range(n_rows):
                for col in range(n_cols):
                    if self.tableWidget.item(row, col).isSelected():
                        indices.append(row)
                        break
            self.plt_data.drop_row(indices)
            for _ in range(len(indices)):
                self.tableWidget.removeRow(0)

        with threading.Lock():
            dropSelectedRow()
            self.updateTableContent()


    def dropif(self):
        command = self.condition_entry.text()
        if self.cln_selected_col_checkbox.isChecked():
            selected_cols = get_selected_columns(self.tableWidget)
        else:
            selected_cols = [0, 1]
        self.plt_data.dropif(cleaning.clean(command, selected_cols))
        self.tableWidget.setRowCount(self.plt_data.shape()[0])
        self.updateTableContent()


    def reset(self):
        self.plt_data.reset()
        n_rows, n_cols = self.plt_data.shape()
        self.tableWidget.setRowCount(n_rows)
        self.tableWidget.setColumnCount(n_cols)
        self.updateTableContent()



if __name__ == '__main__':
    do = read_csv("titanic.csv")
    plt_d = PlotData(do)

    app = QApplication([])
    data_handler = PltDataHandler(plt_d)
    data_handler.show()
    app.exec()
