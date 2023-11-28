from PyQt5.QtWidgets import QApplication

from application import data_handler, main_window, mpl_canvas, data_tab
from logic import data_object



if __name__ == "__main__":
    app = QApplication([])

    d_obj = data_object.read_csv("diabetes.csv")
    d_handler = data_handler.DataHandler(d_obj)
    canvas = mpl_canvas.MPLCanvas(d_obj)
    d_tab = data_tab.DataTab(d_handler)
    window = main_window.MainWindow(canvas, d_tab, d_obj)

    # d_handler.show()
    window.show()

    app.exec_()