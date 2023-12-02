from dataclasses import dataclass
from typing import Callable
import numpy as np
import statsmodels.api as sm

from logic.plot_data import PlotData

@dataclass
class Regression:
    intercept: float
    coef: float
    degree: int
    type: str
    link: Callable


def fit(plt_data: PlotData, family: str):
    match family:
        case "linear": 
            f = sm.families.Gaussian()
            func = lambda x: x
        case "logistic":
            f = sm.families.Binomial()
            func = lambda x: 1 / (1 + np.exp(-x))

    
    X = sm.add_constant(plt_data.get_X_col())
    y = plt_data.get_Y_col()
    model = sm.GLM(y, X, family=f)
    result = model.fit()

    intercept = result.params[0]
    coef = result.params[1]

    return Regression(intercept, coef, 1, family, func)

