from data_loader import DataLoader
from scipy import interpolate
from scipy.interpolate import CubicSpline, PchipInterpolator, UnivariateSpline
import numpy as np
import pandas as pd
import matplotlib .pyplot as plt



class Interpolator():
    """Class implementing multiple interpolators"""

    def __init__(self, x, y, method):
        self.x = x
        self.y = y
        self.method = method


    def linear_interpolator(self):





if __name__ == "__main__":

    # # linear interpolator
    # path_data = './data/datos.csv'
    # data = DataLoader(path_data)
    # q_gl,q_fluid_wells = data.load_data()
    # df = pd.DataFrame(q_fluid_wells)
    # df = df.transpose()
    # well1 = df[1]
    # max_value_axis = max(q_gl)

    # injection_rates_range = np.arange(0,max_value_axis,10)
    # print(injection_rates_range)
    # linterp = np.interp(injection_rates_range, q_gl, well1)

    # #plt.plot(q_gl, well1, 'o', color= 'red')
    # plt.plot(injection_rates_range, linterp)
    # plt.show()



    path_data = './data/datos.csv'
    data = DataLoader(path_data)
    q_gl,q_fluid_wells = data.load_data()
    df = pd.DataFrame(q_fluid_wells)
    df = df.transpose()
    well1 = df[3]
    max_value_axis = max(q_gl)

    injection_rates_range = np.arange(0,max_value_axis,10)

    spl = CubicSpline(q_gl, well1)
    pchip_interp = PchipInterpolator(q_gl, well1)
    univar_spl = UnivariateSpline(q_gl, well1, s=10)

    linterp = np.interp(injection_rates_range, q_gl, well1)

    print(injection_rates_range)

    interpolated_prod_rates_spl = np.round(spl(injection_rates_range),0)
    interpolated_prod_rates_pchip = np.round(pchip_interp(injection_rates_range),0)
    interpolated_prod_rates_univar = np.round(univar_spl(injection_rates_range),0)
    interpolated_prod_rates_linterp = np.round(univar_spl(injection_rates_range),0)

    #plt.plot(q_gl, well1, 'o', color= 'red')
    #plt.plot(injection_rates_range, interpolated_prod_rates_spl, label='spl')
    plt.plot(injection_rates_range, interpolated_prod_rates_pchip, label ='pchip')
    #plt.plot(injection_rates_range, interpolated_prod_rates_univar, label='univar')
    plt.plot(injection_rates_range, linterp, label='interp')

    plt.legend()
    plt.show()
