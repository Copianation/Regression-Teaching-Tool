from PyQt5.QtWidgets import QTabWidget


class DataTab(QTabWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.addTab(data_handler, "Data Queries")