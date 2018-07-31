import numpy as np
import pandas as pd

class DatafileFormated:
    """
        responsble for preprocess data
        get_x_y_name and corresponding data
    """
    chart_name = None
    # number of x_y
    num_x = None
    num_y = None
    # index for X and Y
    Y_cols = None
    X_cols = None

    y_names = None
    display_Xname = None
    datafile = None

    # Y_names
    def __init__(self, datafile, chart_name):

        self.datafile = datafile
        self.chart_name = chart_name
        self.Y_cols = [x for x in datafile.columns if x.startswith('Y')]
        self.X_cols = [x for x in datafile.columns if x.startswith('X')]
        self.num_x = len(self.X_cols)
        self.num_y = len(self.Y_cols)
        self.display_X = self.X_cols[-1]
        self.display_Xname = datafile[self.display_X][0]
        self.length = datafile.shape[0] - 1
        self.elements = self.length * self.num_y
        self.y_names = [datafile[x][0] for x in self.Y_cols]


        if self.display_Xname == "DATE RANGE":
            self.datafile[self.display_X].loc[1:] = pd.to_datetime(datafile[self.display_X].loc[1:]).dt.strftime('%Y-%m').values
            self.datafile.loc[1:] = self.datafile.loc[1:].sort_values(self.display_X).values



    def get_data(self, cols_index):
        return self.datafile[cols_index][1:].values.astype(np.float)

    def get_name(self, cols_index):
        return self.datafile[cols_index][0]

    def get_x_name(self, row_index):
        return [self.datafile[x][0] + "_" + self.datafile[x][row_index + 1] for x in self.X_cols]

    def get_date(self):
        key = self.datafile.columns[np.where(self.datafile.loc[1, :])[0]][0]
        return self.datafile[key][1:].values