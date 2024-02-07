from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
from sklearn.neural_network import MLPRegressor

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QCheckBox)

from logic.plot_data import *
from logic.regression import Regression
from util.app_util import *


class MPLCanvas(QWidget):
    def __init__(self, plt_data: PlotData, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(800)

        self.plt_data = plt_data

        fig = Figure(figsize=(8, 8))
        self.can = FigureCanvasQTAgg(fig)
        self.plot_btn = btn_factory('Plot', self.plot)
        self.plot_X_btn = btn_factory('Plot X', self.plot_X)
        self.plot_Y_btn = btn_factory('Plot Y', self.plot_Y)
        self.show_train = QCheckBox("Show train data")
        self.show_test = QCheckBox("Show test data")
        self.show_train.setChecked(True)
        self.show_test.setChecked(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.can)
        layout.addLayout(couple_layout(self.show_train, self.show_test))
        layout.addWidget(self.plot_btn)
        layout.addLayout(couple_layout(self.plot_X_btn, self.plot_Y_btn))
        
        self.ax = self.can.figure.add_subplot(111)

    def plot(self):
        self.ax.cla()

        show_train = self.show_train.isChecked()
        show_test = self.show_test.isChecked()

        x_label = self.plt_data.columns()[1]
        y_label = self.plt_data.columns()[0]

        if show_train:
            self.ax.scatter(self.plt_data.x_train, self.plt_data.y_train, label=f"Train data:{x_label} - {y_label}",
                            c="blue")
        if show_test:
            self.ax.scatter(self.plt_data.x_test, self.plt_data.y_test, label=f"Test data:{x_label} - {y_label}",
                            c="orange")

        self.ax.grid(True)
        self.ax.legend()
        self.can.figure.tight_layout()
        self.can.draw()

    def plot_X(self):
        self.ax.cla()

        self.ax.hist(self.plt_data.get_X_col(), bins=20)
        self.ax.set_xlabel(self.plt_data.columns()[1])
        self.can.figure.tight_layout()
        self.can.draw()

    def plot_Y(self):
        self.ax.cla()

        self.ax.hist(self.plt_data.get_Y_col(), bins=20)
        self.ax.set_xlabel(self.plt_data.columns()[0])
        self.can.figure.tight_layout()
        self.can.draw()

    def plot_regression(self, regression: Regression):
        self.plot()
        intercept = regression.intercept
        coef = regression.coef
        degree = regression.degree

        min = np.min(self.plt_data.get_X_col())
        max = np.max(self.plt_data.get_X_col())

        x = np.linspace(min, max, 100)
        polynomial = intercept + np.sum([coef[i] * np.power(x, i+1) for i in range(0, degree)], axis=0)
        y = regression.link(polynomial)

        self.ax.plot(x, y, color = "green", label = f"{regression.type} regression")
        self.ax.legend()
        self.can.draw()

    def plot_ann_model(self, model: MLPRegressor):
        self.plot()
        min = np.min(self.plt_data.get_X_col())
        max = np.max(self.plt_data.get_X_col())

        x = np.linspace(min, max, 100).reshape(-1, 1)
        y = model.predict(x)
        self.ax.plot(x, y, color = "green", label = f"ANN")
        self.ax.legend()
        self.can.draw()
