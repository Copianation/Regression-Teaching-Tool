from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton)

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from logic.data_object import *
from util.app_util import *


class MPLCanvas(QWidget):
    def __init__(self, data_obj: DataObject, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(800)

        self.data_obj = data_obj

        fig = Figure(figsize=(8, 8))
        self.can = FigureCanvasQTAgg(fig)
        self.plot_btn = btn_factory('Plot relation', self.plot_relation)
        self.plot_X_btn = btn_factory('Plot X', self.plot_X)
        self.plot_Y_btn = btn_factory('Plot Y', self.plot_Y)

        layout = QVBoxLayout(self)
        layout.addWidget(self.can)
        layout.addWidget(self.plot_btn)
        layout.addWidget(self.plot_X_btn)
        layout.addWidget(self.plot_Y_btn)
        
        self.ax = self.can.figure.add_subplot(111)

    def plot_relation(self):
        self.ax.cla()

        label = f"{self.data_obj.columns()[self.data_obj.X]} - {self.data_obj.columns()[self.data_obj.Y]}"
        self.ax.scatter(self.data_obj.get_X_col(), self.data_obj.get_Y_col(), label=label)
        self.ax.grid(True)
        self.ax.legend()
        self.can.figure.tight_layout()
        self.can.draw()

    def plot_X(self):
        self.ax.cla()

        label = f"{self.data_obj.columns()[self.data_obj.X]}"
        self.ax.hist(self.data_obj.get_X_col(), label=label, bins=20)
        self.ax.legend()
        self.can.figure.tight_layout()
        self.can.draw()

    def plot_Y(self):
        self.ax.cla()

        label = f"{self.data_obj.columns()[self.data_obj.Y]}"
        self.ax.hist(self.data_obj.get_Y_col(), label=label, bins=20)
        self.ax.legend()
        self.can.figure.tight_layout()
        self.can.draw()