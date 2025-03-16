from data_loader import DataLoader
from scipy import interpolate
from scipy.interpolate import CubicSpline, PchipInterpolator, UnivariateSpline
import numpy as np
import pandas as pd
import matplotlib .pyplot as plt



class Interpolator():
    """Class implementing multiple interpolators"""

    def __init__(self, x, y):
        self.x_values_given = x
        self.y_values_given = y

    def linear_interpolator(self):
        """Linear interpolator between x and x_max, in steps of 10"""
        x_axis_values = np.arange(0, max(self.x_values_given), 10)
        lin_interp = np.interp(x_axis_values, self.x_values_given, self.y_values_given)
        return x_axis_values, lin_interp

    def pchip_interpolator(self):
        """Pchip interpolator"""
        x_axis_values = np.arange(0, max(self.x_values_given), 10)
        pchip_interp = PchipInterpolator(self.x_values_given, self.y_values_given)
        interpolated_y_values = np.round(pchip_interp(x_axis_values),0)
        return x_axis_values, interpolated_y_values

    def spline_interpolator(self):
        """Spline interpolator"""
        x_axis_values = np.arange(0, max(self.x_values_given), 10)
        spl = CubicSpline(self.x_values_given, self.y_values_given)
        interpolated_y_values = np.round(spl(x_axis_values),0)
        return x_axis_values, interpolated_y_values

    def univariate_spline_interpolator(self):
        """Univar interpolator"""
        x_axis_values = np.arange(0, max(self.x_values_given), 10)
        univar_spl = UnivariateSpline(self.x_values_given, self.y_values_given, s=10)
        interpolated_y_values = np.round(univar_spl(x_axis_values),0)
        return x_axis_values, interpolated_y_values


if __name__ == "__main__":

    # linear interpolator
    path_data = './data/datos.csv'
    data = DataLoader(path_data)
    q_gl, q_fluid_wells = data.load_data()
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


    lininterp = Interpolator(q_gl, q_fluid_wells[0])
    result = lininterp.linear_interpolator()
    print(result)
    plt.plot(result[0], result[1])


    pchip = Interpolator(q_gl, q_fluid_wells[0])
    result_pchip = pchip.pchip_interpolator()
    plt.plot(result_pchip[0], result_pchip[1])

    spl = Interpolator(q_gl, q_fluid_wells[0])
    result_spl = spl.spline_interpolator()
    plt.plot(result_spl[0], result_spl[1])

    univar = Interpolator(q_gl, q_fluid_wells[0])
    result_univar = spl.univariate_spline_interpolator()
    plt.plot(result_univar[0], result_univar[1])

    #plt.plot(q_gl, q_fluid_wells[0], 'o', color= 'red')

    plt.show()

    # path_data = './data/datos.csv'
    # data = DataLoader(path_data)
    # q_gl,q_fluid_wells = data.load_data()
    # df = pd.DataFrame(q_fluid_wells)
    # df = df.transpose()
    # well1 = df[3]
    # max_value_axis = max(q_gl)

    # injection_rates_range = np.arange(0,max_value_axis,10)

    # spl = CubicSpline(q_gl, well1)
    # pchip_interp = PchipInterpolator(q_gl, well1)
    # univar_spl = UnivariateSpline(q_gl, well1, s=10)

    # linterp = np.interp(injection_rates_range, q_gl, well1)

    # print(injection_rates_range)

    # interpolated_prod_rates_spl = np.round(spl(injection_rates_range),0)
    # interpolated_prod_rates_pchip = np.round(pchip_interp(injection_rates_range),0)
    # interpolated_prod_rates_univar = np.round(univar_spl(injection_rates_range),0)
    # interpolated_prod_rates_linterp = np.round(univar_spl(injection_rates_range),0)

    # #plt.plot(q_gl, well1, 'o', color= 'red')
    # #plt.plot(injection_rates_range, interpolated_prod_rates_spl, label='spl')
    # plt.plot(injection_rates_range, interpolated_prod_rates_pchip, label ='pchip')
    # #plt.plot(injection_rates_range, interpolated_prod_rates_univar, label='univar')
    # plt.plot(injection_rates_range, linterp, label='interp')

    # plt.legend()
    # plt.show()
