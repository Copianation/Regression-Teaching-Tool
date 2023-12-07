from PyQt5.QtWidgets import QApplication

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from application import main_window, mpl_canvas, data_tab
from application.tabs import data_handler, plot_data_handler, regression_controller
from logic import data_object, plot_data



if __name__ == "__main__":
    app = QApplication([])

    d_obj = data_object.read_csv("diabetes.csv")
    plt_data = plot_data.PlotData(d_obj)

    canvas = mpl_canvas.MPLCanvas(plt_data)

    plt_d_handler = plot_data_handler.PltDataHandler(plt_data)
    d_handler = data_handler.DataHandler(d_obj, plt_data, plt_d_handler)
    rg_control = regression_controller.RGController(plt_data, canvas)
    d_tab = data_tab.DataTab(d_handler, plt_d_handler, rg_control)
    
    window = main_window.MainWindow(canvas, d_tab, d_obj)

    window.show()

    app.exec_()