import pandas as pd

import numpy as np

from sklearn.model_selection import train_test_split

from logic.data_object import *


class PlotData():
    def __init__(self, data_obj: DataObject):
        self.data_obj = data_obj
        self.plt_df = data_obj.get_plot_dataframe()
        self.default_split()

    def train_test_split(self, test_size):
        if test_size == 0:
            self.default_split()
            return
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.get_X_col(), self.get_Y_col(), test_size=test_size) 

    def default_split(self):
        self.x_train = self.get_X_col()
        self.y_train = self.get_Y_col()
        self.x_test = []
        self.y_test = []

    def retrieve_plt_df(self):
        self.original_plt_df = self.data_obj.get_plot_dataframe()
        self.plt_df = self.data_obj.get_plot_dataframe()
        self.default_split()

    def get_X_col(self):
        return self.plt_df.iloc[:, 1].values.reshape(-1, 1)
    
    def get_Y_col(self):
        return self.plt_df.iloc[:, 0].values.reshape(-1, 1) 

    def drop_row(self, indices):
        self.plt_df.drop(indices, inplace=True)
        self.plt_df.reset_index(drop=True, inplace=True)

    def dropna(self):
        self.plt_df.dropna(inplace=True)
        self.plt_df.reset_index(drop=True, inplace=True)

    def reset(self):
        self.plt_df = self.original_plt_df.copy()

    def dropif(self, func):
        """
        func(df: pd.DataFrame) -> indices to drop
        """
        if func is None: return
        self.plt_df.drop(func(self.plt_df), inplace=True)
        self.plt_df.reset_index(drop=True, inplace=True)

    def columns(self):
        return self.plt_df.columns

    def shape(self):
        return self.plt_df.shape
    
    def iloc(self, row, col):
        return self.plt_df.iloc[row, col]