from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure

import pandas as pd

from PyQt5.QtWidgets import (QWidget, QVBoxLayout)

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from logic.data_object import *


class MPLCanvas(QWidget):
    def __init__(self, data_obj: DataObject, parent=None):
        super().__init__(parent)

        self.data_obj = data_obj

        fig = Figure(figsize=(8, 8))
        self.can = FigureCanvasQTAgg(fig)
        self.toolbar = NavigationToolbar2QT(self.can, self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.can)

        # here you can set up your figure/axis
        self.ax = self.can.figure.add_subplot(111)

    def plot_data(self):
        # plot a basic line plot from x and y values.
        self.ax.cla() # clears the axis

        label = f"{self.data_obj.columns()[self.data_obj.X]} - {self.data_obj.columns()[self.data_obj.Y]}"
        self.ax.scatter(self.data_obj.get_X_col(), self.data_obj.get_Y_col(), label=label)
        self.ax.grid(True)
        self.ax.legend()
        self.can.figure.tight_layout()
        self.can.draw()