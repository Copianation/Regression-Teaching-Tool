from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QMainWindow, QMenuBar, QMenu, QWidget
import pandas as pd

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from logic.data_object import *
from application.mpl_canvas import MPLCanvas


class MainWindow(QMainWindow):
    def __init__(self, canvas: MPLCanvas, data_obj: DataObject = None):
        super().__init__()

        self.setWindowTitle('Main Window')
        self.resize(800, 1000)

        self.data_obj = data_obj

        self.canvas = canvas

        self.btn_plot1 = QPushButton('plot1', self)
        self.btn_plot1.clicked.connect(self.canvas.plot_data)


        self.btn_plot2 = QPushButton('plot2', self)
        self.btn_plot3 = QPushButton('scatter', self)

        self.layout()
    
    def layout(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_plot1)
        layout.addWidget(self.btn_plot2)
        layout.addWidget(self.btn_plot3)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)



if __name__ == '__main__':
    d_obj = DataObject()
    app = QApplication([])
    canvas = MPLCanvas(d_obj)
    qt_app = MainWindow(canvas, d_obj)
    qt_app.show()
    app.exec_()