import pandas as pd


import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from logic.data_object import *


class PlotData():
    def __init__(self, data_obj: DataObject):
        self.data_obj = data_obj
        self.original_plt_df = data_obj.get_plot_dataframe()
        self.plt_df = data_obj.get_plot_dataframe()
        self.transformation = "none"


    def retrieve_plt_df(self):
        self.original_plt_df = self.data_obj.get_plot_dataframe()
        self.plt_df = self.data_obj.get_plot_dataframe()

    def get_X_col(self):
        return self.plt_df.iloc[:, 1]
    
    def get_Y_col(self):
        return self.plt_df.iloc[:, 0]

    def drop_row(self, indices):
        self.plt_df.drop(indices, inplace=True)
        self.plt_df.reset_index(drop=True, inplace=True)

    def dropna(self):
        self.plt_df.dropna(inplace=True)
        self.plt_df.reset_index(drop=True, inplace=True)

    def reset(self):
        self.plt_df = self.original_plt_df.copy()

    def columns(self):
        return self.plt_df.columns

    def shape(self):
        return self.plt_df.shape
    
    def iloc(self, row, col):
        return self.plt_df.iloc[row, col]