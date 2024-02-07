from keras import models
from keras import layers

from logic.plot_data import PlotData

def fit(plt_data: PlotData, layer_data):

    model = models.Sequential()

    first_layer = True
    for N in layer_data:
        if first_layer:
            model.add(layers.Dense(N, activation="relu", input_shape=(1, )))
            first_layer = False
        else:
            model.add(layers.Dense(N, activation="relu"))
    model.add(layers.Dense(1, activation="relu"))

    model.compile(optimizer='adam', loss='mean_squared_error')
    history = model.fit(plt_data.x_train, plt_data.y_train, epochs=10, batch_size=32, verbose=2)

    return model, history

def get_model_summary(model):
    string_list = []
    model.summary(line_length=50, print_fn=lambda x: string_list.append(x))
    return "\n".join(string_list)