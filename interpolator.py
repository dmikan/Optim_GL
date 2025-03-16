from data_loader import DataLoader
from scipy import interpolate
from scipy.interpolate import CubicSpline, PchipInterpolator, UnivariateSpline
import numpy as np
import pandas as pd
import matplotlib .pyplot as plt



class Interpolator():
    """Class implementing multiple interpolators"""

    def __init__(self, x, y, step):
        self.x_values_given = x
        self.y_values_given = y
        self.step = step

    def linear_interpolator(self):
        """Linear interpolator between x and x_max, in steps of 10"""
        x_axis_values = np.arange(0, max(self.x_values_given) + self.step, self.step)
        lin_interp = np.interp(x_axis_values, self.x_values_given, self.y_values_given)
        interpolated_y_values = np.round(lin_interp, 0)
        return x_axis_values, interpolated_y_values

    def pchip_interpolator(self):
        """Pchip interpolator"""
        x_axis_values = np.arange(0, max(self.x_values_given) + self.step, self.step)
        pchip_interp = PchipInterpolator(self.x_values_given, self.y_values_given)
        interpolated_y_values = np.round(pchip_interp(x_axis_values),0)
        return x_axis_values, interpolated_y_values

    def spline_interpolator(self):
        """Spline interpolator"""
        x_axis_values = np.arange(0, max(self.x_values_given) + self.step, self.step)
        spl = CubicSpline(self.x_values_given, self.y_values_given)
        interpolated_y_values = np.round(spl(x_axis_values),0)
        return x_axis_values, interpolated_y_values

    def univariate_spline_interpolator(self):
        """Univar interpolator"""
        x_axis_values = np.arange(0, max(self.x_values_given) + self.step, self.step)
        univar_spl = UnivariateSpline(self.x_values_given, self.y_values_given, s=1)
        interpolated_y_values = np.round(univar_spl(x_axis_values),0)
        return x_axis_values, interpolated_y_values


if __name__ == "__main__":

    # linear interpolator
    path_data = './data/datos.csv'
    data = DataLoader(path_data)
    q_gl, q_fluid_wells = data.load_data()

    print(q_gl)
    print(q_fluid_wells)

    lininterp = Interpolator(q_gl, q_fluid_wells[1], 1)
    result = lininterp.linear_interpolator()
    #print(result)
    #plt.plot(result[0], result[1], label= 'linear')


    pchip = Interpolator(q_gl, q_fluid_wells[1], 1)
    result_pchip = pchip.pchip_interpolator()
    plt.plot(result_pchip[0], result_pchip[1], label= 'pchip')
    print(result_pchip)

    spl = Interpolator(q_gl, q_fluid_wells[1], 1)
    result_spl = spl.spline_interpolator()
    #plt.plot(result_spl[0], result_spl[1], label='spline')

    univar = Interpolator(q_gl, q_fluid_wells[1], 1)
    result_univar = univar.univariate_spline_interpolator()
    #plt.plot(result_univar[0], result_univar[1], label= 'univar_spl')

    plt.plot(q_gl, q_fluid_wells[1], 'o', color= 'red')
    plt.legend()

    plt.show()
