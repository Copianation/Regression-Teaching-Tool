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
            self.train_tableWidget = QTableWidget(20, 2)
            self.test_tableWidget = QTableWidget(20, 2)
            return
        n_rows, _ = self.plt_data.shape()
        self.train_tableWidget = QTableWidget(n_rows, 2)
        self.test_tableWidget = QTableWidget(n_rows, 2)

        self.updateTableContent()


    def updateTableContent(self):
        train_header = ["train Y: " + self.plt_data.columns()[0], "train X: " + self.plt_data.columns()[1]]
        test_header = ["test Y: " + self.plt_data.columns()[0], "test X: " + self.plt_data.columns()[1]]
        self.train_tableWidget.setHorizontalHeaderLabels(train_header)
        self.test_tableWidget.setHorizontalHeaderLabels(test_header)
        n_train = len(self.plt_data.x_train)
        n_test = len(self.plt_data.x_test)
        self.train_tableWidget.setRowCount(n_train)
        self.test_tableWidget.setRowCount(n_test)
        for row in range(n_train):
            x_item = QTableWidgetItem(str(self.plt_data.x_train[row, 0]))
            y_item = QTableWidgetItem(str(self.plt_data.y_train[row, 0]))
            self.train_tableWidget.setItem(row, 0, y_item)
            self.train_tableWidget.setItem(row, 1, x_item)
        for row in range(n_test):
            x_item = QTableWidgetItem(str(self.plt_data.x_test[row, 0]))
            y_item = QTableWidgetItem(str(self.plt_data.y_test[row, 0]))
            self.test_tableWidget.setItem(row, 0, y_item)
            self.test_tableWidget.setItem(row, 1, x_item)

    
    def createButtons(self):
        self.drop_row_btn = btn_factory("Delete row", self.dropRow)
        self.clean_btn = btn_factory("Drop if", self.dropif)
        self.reset_btn = btn_factory("Reset data", self.reset)
        self.condition_entry = QLineEdit()
        self.split_btn = btn_factory("Split", self.split)
        self.split_size_entry = QLineEdit()
        self.cln_selected_col_checkbox = QCheckBox("Only clean selected columns")
        self.cln_selected_col_checkbox.setChecked(True)


    def layout(self):
        group_list = []
        group_list.append(group_box_factory("Table Adjustment", self.drop_row_btn))

        split_layout = couple_layout(self.split_btn, self.split_size_entry)
        group_list.append(group_box_factory("Train Test Split", split_layout))
        
        cleaning_layout = couple_layout(self.clean_btn, self.condition_entry)
        group_list.append(group_box_factory("Data Cleaning", self.cln_selected_col_checkbox, cleaning_layout))

        control_layout = QVBoxLayout()
        control_layout.addStretch()
        for group in group_list:
            control_layout.addWidget(group)
        control_layout.addWidget(self.reset_btn)

        layout = QGridLayout()
        layout.addLayout(control_layout, 0, 2, 4, 2)

        self.train_tableWidget.setMinimumWidth(200)
        layout.addWidget(self.train_tableWidget, 0, 0, 4, 1)
        self.test_tableWidget.setMinimumWidth(200)
        layout.addWidget(self.test_tableWidget, 0, 1, 4, 1)

        self.setLayout(layout)

    def split(self):
        def is_float(string: str):
            return string.replace(".", "").isnumeric()

        text = self.split_size_entry.text().strip()
        if is_float(text):
            test_size = float(text)
        else: test_size = 0
        self.plt_data.train_test_split(test_size)
        self.updateTableContent()

    def dropRow(self):
        def dropSelectedRow():
            indices = []
            n_rows, n_cols = self.plt_data.shape()
            for row in range(n_rows):
                for col in range(n_cols):
                    if self.train_tableWidget.item(row, col).isSelected():
                        indices.append(row)
                        break
            self.plt_data.drop_row(indices)
            for _ in range(len(indices)):
                self.train_tableWidget.removeRow(0)

        with threading.Lock():
            dropSelectedRow()
            self.updateTableContent()


    def dropif(self):
        command = self.condition_entry.text()
        if self.cln_selected_col_checkbox.isChecked():
            selected_cols = get_selected_columns(self.train_tableWidget)
        else:
            selected_cols = [0, 1]
        self.plt_data.dropif(cleaning.clean(command, selected_cols))
        self.train_tableWidget.setRowCount(self.plt_data.shape()[0])
        self.updateTableContent()


    def reset(self):
        self.plt_data.reset()
        n_rows, n_cols = self.plt_data.shape()
        self.train_tableWidget.setRowCount(n_rows)
        self.train_tableWidget.setColumnCount(n_cols)
        self.updateTableContent()



if __name__ == '__main__':
    do = read_csv("titanic.csv")
    plt_d = PlotData(do)

    app = QApplication([])
    data_handler = PltDataHandler(plt_d)
    data_handler.show()
    app.exec()
