from PyQt5.QtWidgets import (QApplication, QPushButton, QVBoxLayout,
            QGridLayout, QMainWindow, QMenuBar, QMenu, QWidget)
import pandas as pd

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from logic.data_object import *
from application.mpl_canvas import MPLCanvas
from application.data_handler import DataHandler


def layout(layout_func):
    def wrapper(self: QMainWindow, *args, **kwargs):
        central_widget = QWidget(self)
        central_widget.setLayout(layout_func(self, *args, **kwargs))
        self.setCentralWidget(central_widget)
    return wrapper


class MainWindow(QMainWindow):
    def __init__(self, canvas: MPLCanvas, data_handler: DataHandler, data_obj: DataObject = None):
        super().__init__()

        self.setWindowTitle('Main Window')
        self.resize(1200, 1000)

        self.data_obj = data_obj

        self.canvas = canvas
        self.data_handler = data_handler

        self.btn_plot = QPushButton('plot', self)
        self.btn_plot.clicked.connect(self.canvas.plot_data)

        self.add_data_handler()

    @layout
    def default_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_plot)
        return layout

    @layout
    def add_data_handler(self):
        layout = QGridLayout()
        layout.addWidget(self.canvas, 0, 0, 1, 1)
        layout.addWidget(self.btn_plot)
        layout.addWidget(self.data_handler, 0, 1, 3, 2)
        return layout




if __name__ == '__main__':
    d_obj = DataObject()
    app = QApplication([])
    canvas = MPLCanvas(d_obj)
    d_handler = DataHandler(d_obj)
    qt_app = MainWindow(canvas, d_handler, d_obj)
    qt_app.show()
    app.exec_()