from PyQt5.QtWidgets import QTabWidget


class DataTab(QTabWidget):
    def __init__(self, data_handler, plt_data_handler, rg_control):
        super().__init__()
        self.addTab(data_handler, "Data Queries")
        self.addTab(plt_data_handler, "Plot Data")
        self.addTab(rg_control, "Regression")