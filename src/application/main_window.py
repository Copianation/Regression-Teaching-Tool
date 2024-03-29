from PyQt5.QtWidgets import (QApplication, QPushButton, QVBoxLayout,
            QGridLayout, QMainWindow, QMenuBar, QMenu, QWidget, QSplitter,
            QHBoxLayout)
from PyQt5.QtCore import Qt

from logic.data_object import *
from application.mpl_canvas import MPLCanvas
from application.data_tab import DataTab


def layout(layout_func):
    def wrapper(self: QMainWindow, *args, **kwargs):
        central_widget = QWidget(self)
        central_widget.setLayout(layout_func(self, *args, **kwargs))
        self.setCentralWidget(central_widget)
    return wrapper


class MainWindow(QMainWindow):
    def __init__(self, canvas: MPLCanvas, data_tab: DataTab, data_obj: DataObject = None):
        super().__init__()

        self.setWindowTitle('Regression Tool')
        self.resize(1400, 1000)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.data_obj = data_obj

        self.canvas = canvas
        self.data_tab = data_tab

        self.add_data_tab()

    @layout
    def default_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.canvas)
        return layout

    @layout
    def add_data_tab(self):
        layout = QHBoxLayout()
        splitter = QSplitter()
        splitter.setHandleWidth(20)
        splitter.addWidget(self.canvas)
        splitter.addWidget(self.data_tab)
        layout.addWidget(splitter)
        return layout