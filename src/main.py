from PyQt5.QtWidgets import QApplication

from application import data_handler, plot_data_handler, main_window, mpl_canvas, data_tab
from logic import data_object, plot_data



if __name__ == "__main__":
    app = QApplication([])

    d_obj = data_object.read_csv("diabetes.csv")
    plt_data = plot_data.PlotData(d_obj)

    plt_d_handler = plot_data_handler.PltDataHandler(plt_data)
    d_handler = data_handler.DataHandler(d_obj, plt_data, plt_d_handler)
    d_tab = data_tab.DataTab(d_handler, plt_d_handler)

    canvas = mpl_canvas.MPLCanvas(plt_data)
    
    window = main_window.MainWindow(canvas, d_tab, d_obj)

    # d_handler.show()
    window.show()

    app.exec_()