import pandas as pd


def read_csv(path: str):
    return DataObject(pd.read_csv(path))

class DataObject():
    def __init__(self, df: pd.DataFrame = None):
        if df is None:
            df = pd.DataFrame(0, index=range(8), columns=['X', 'Y'])

        self.df = df
        self.X = 0
        self.Y = 1
        self.omit = []

    def get_X_col(self):
        return self.df.iloc[:, self.X]
    
    def get_Y_col(self):
        return self.df.iloc[:, self.Y]

    def drop_row(self, indices):
        self.df.drop(indices, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def drop_col(self, indices):
        self.df.drop(self.df.columns[indices], axis=1, inplace=True)
        self.df.reset_index(drop=True, inplace=True)
    
    def columns(self):
        return self.df.columns

    def shape(self):
        return self.df.shape
    
    def iloc(self, row, col):
        return self.df.iloc[row, col]

    def set_df(self, df: pd.DataFrame):
        self.df = df

    def setX(self, X: int):
        self.X = X

    def setY(self, Y: int):
        self.Y = Y