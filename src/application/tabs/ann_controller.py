from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
        QTableWidget, QGridLayout, QGroupBox, QLabel, QTextEdit,
        QVBoxLayout, QComboBox)
from PyQt5.QtCore import Qt

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

        self.create_buttons()
        self.create_history_canvas()
        self.layout()


    def create_buttons(self):
        self.fit_btn = btn_factory("fit", self.fit_plt_data)
        self.famile_cbbox = QComboBox()
        self.famile_cbbox.addItems(["linear", "logistic", "poisson"])
        self.hidden_layer_entry = QLineEdit()
        self.summary = QTextEdit()
        font = self.summary.currentFont()
        font.setPointSize(10)
        self.summary.setCurrentFont(font)

    def create_history_canvas(self): 
        fig = Figure(figsize=(6, 6))
        self.history_can = FigureCanvasQTAgg(fig)
        self.history_ax = self.history_can.figure.add_subplot(111)

    def layout(self):
        hidden_layer_label = QLabel("Hidden layer information")

        hidden_layer_layout = couple_layout(hidden_layer_label, self.hidden_layer_entry)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.history_can)
        layout.addWidget(self.summary)
        layout.addLayout(hidden_layer_layout)
        layout.addWidget(self.fit_btn)

        self.setLayout(layout)

    def fit_plt_data(self):
        layer_data = string_to_num_list(self.hidden_layer_entry.text())
        if layer_data is None:
            return

        model, history = ann.fit(self.plt_data, layer_data)
        loss_history = history.history['loss']

        self.summary.setText(ann.get_model_summary(model))

        self.canvas.plot_ann_model(model)
        
        self.history_ax.cla()
        self.history_ax.plot(loss_history)
        self.history_ax.set_xlabel("Epoch")
        self.history_ax.set_ylabel("Loss")
        self.history_can.figure.tight_layout()
        self.history_can.draw()