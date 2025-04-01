from data_loader import DataLoader
import numpy as np
import pandas as pd
import matplotlib .pyplot as plt
from scipy.optimize import curve_fit



class Fitting():
    """Class implementing fitting of performances curves"""

    def __init__(self, q_gl, q_prod):
        self.q_gl = q_gl
        self.q_prod = q_prod

    def fit(self):
        params_list = curve_fit(self.model, self.q_gl, self.q_prod)
        return params_list[0]


    def model(self, q_gl, a, b, c, d, e):
        #q_gl = np.array(self.q_gl)
        return a + b * q_gl + c * (q_gl ** 0.7) + d * np.log(q_gl + 0.9) + e * np.exp(-(q_gl ** 0.6))



if __name__ == "__main__":
    load = DataLoader('./data/gl sensitivity template.csv')
    var1 = load.load_data_gl_template()
    q_gl1 = var1[0][0]
    q_prod1 = var1[1][0]
    X = np.array([125, 250, 500, 625, 875])
    y = np.array([0, 186.42, 216.41, 194.81, 127.12])


    fitter = Fitting(X, y)
    a,b,c,d,e = fitter.fit()


    q_gl_range = np.linspace(125, 1250, 500)
    y_pred = fitter.model(q_gl_range, a, b, c, d, e)

    #print(q_gl_range)
    print((y_pred))
    plt.plot(q_gl_range, y_pred)
    plt.show()
