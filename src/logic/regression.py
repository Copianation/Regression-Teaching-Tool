from dataclasses import dataclass
from typing import Callable, List
import numpy as np
import pandas as pd
import statsmodels.api as sm

from logic.plot_data import PlotData

@dataclass
class Regression:
    summary: str
    intercept: float
    coef: List[float]
    degree: int
    type: str
    link: Callable


def fit(plt_data: PlotData, family: str, degree: int):
    match family:
        case "linear": 
            f = sm.families.Gaussian()
            func = lambda x: x
        case "logistic":
            f = sm.families.Binomial()
            func = lambda x: 1 / (1 + np.exp(-x))
        case "poisson":
            f = sm.families.Poisson()
            func = np.exp


    columns_with_degree = [np.power(plt_data.get_X_col(), i) for i in range(1, degree+1)]
    X = np.concatenate(columns_with_degree, axis=1)
    X = sm.add_constant(X)
    y = plt_data.get_Y_col()
    model = sm.GLM(y, X, family=f)
    result = model.fit()

    intercept = result.params[0]
    coef = result.params[1:]

    summary = result.summary().as_html()
    summary = summary.replace('<th>', '<th style="font-size:26px">')
    summary = summary.replace('<td>', '<td style="font-size:26px">')
    summary = (
            '<style>'
            'th, td { text-align: left; }'
            'td { padding-right: 20px; }'
            '</style>'
        ) + summary

    return Regression(summary, intercept, coef, degree, family, func)

