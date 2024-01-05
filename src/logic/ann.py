from sklearn.neural_network import MLPRegressor

from logic.plot_data import PlotData


def fit(plt_data: PlotData, hidden_layer):
    model = MLPRegressor(hidden_layer_sizes=hidden_layer, solver = 'lbfgs', learning_rate="adaptive", activation="logistic")
    model.fit(plt_data.get_X_col(), plt_data.get_Y_col().ravel())
    return model