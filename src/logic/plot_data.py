import pandas as pd

from sklearn.linear_model import LinearRegression

from logic.data_object import *


class PlotData():
    def __init__(self, data_obj: DataObject):
        self.data_obj = data_obj
        self.original_plt_df = data_obj.get_plot_dataframe()
        self.plt_df = data_obj.get_plot_dataframe()
        self.transformation = "none"


    
    def linera_regression(self):
        model = LinearRegression()
        model.fit(self.get_X_col(), self.get_Y_col())
        coef = model.coef_[0][0]
        intercept = model.intercept_[0]
        return "linear", coef, intercept


    def retrieve_plt_df(self):
        self.original_plt_df = self.data_obj.get_plot_dataframe()
        self.plt_df = self.data_obj.get_plot_dataframe()

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

    def columns(self):
        return self.plt_df.columns

    def shape(self):
        return self.plt_df.shape
    
    def iloc(self, row, col):
        return self.plt_df.iloc[row, col]