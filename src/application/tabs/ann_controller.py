from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
        QTableWidget, QGridLayout, QGroupBox, QLabel, QTextEdit,
        QVBoxLayout, QComboBox)
from PyQt5.QtCore import Qt
import threading

from application.mpl_canvas import *
from logic.plot_data import *
from logic import ann
from util.app_util import *

class ANNController(QWidget):
    def __init__(self, plt_data: PlotData, canvas: MPLCanvas, parent = None):
        super().__init__(parent)
        self.plt_data = plt_data
        self.canvas = canvas

        self.setWindowTitle("Data Handler")

        self.createButtons()
        self.layout()


    def createButtons(self):
        self.fit_btn = btn_factory("fit", self.fit_plt_data)
        self.famile_cbbox = QComboBox()
        self.famile_cbbox.addItems(["linear", "logistic", "poisson"])
        self.degree_cbbox = QComboBox()
        self.degree_cbbox.addItems([str(i) for i in range(1,6)])
        self.summary = QTextEdit()
        font = self.summary.currentFont()
        font.setPointSize(10)
        self.summary.setCurrentFont(font)

    def layout(self):
        family_label = QLabel("Family=")
        degree_label = QLabel("Degree=")

        family_layout = couple_layout(family_label, self.famile_cbbox)
        degree_layout = couple_layout(degree_label, self.degree_cbbox)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.summary)
        layout.addLayout(family_layout)
        layout.addLayout(degree_layout)
        layout.addWidget(self.fit_btn)

        self.setLayout(layout)

    def fit_plt_data(self):
        model = ann.fit(self.plt_data, [10,4,4], self.summary)
        self.canvas.plot_ann_model(model)