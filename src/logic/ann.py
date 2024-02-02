import io
from contextlib import redirect_stdout
from keras import models
from keras import layers

from logic.plot_data import PlotData

def fit(plt_data: PlotData, layer_data, textbox):

    model = models.Sequential()
    model.add(layers.Dense(16, activation="relu", input_shape=(1, )))
    model.add(layers.Dense(16, activation="sigmoid"))
    model.add(layers.Dense(1, activation="relu"))

    model.compile(optimizer='adam', loss='mean_squared_error')

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        history = model.fit(plt_data.x_train, plt_data.y_train, epochs=10, batch_size=32, verbose=2)
        textbox.setText(buffer.getvalue())
    return model, history