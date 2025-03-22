import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from data_loader import DataLoader
from interpolator import Interpolator
import matplotlib .pyplot as plt
from scipy.interpolate import CubicSpline


class Extrapolator():
    """class implemeting an extrapolator"""

    def __init__(self, x, y, step, upper_bound):
        self.x_values_given = x
        self.y_values_given = y
        self.upper_bound = upper_bound
        self.step = step

    def extrapolate_interp1d(self):
        x_axis_range = np.arange(0, self.upper_bound, self.step)
        #f = interp1d(self.x_values_given, self.y_values_given, kind='linear', fill_value= "extrapolate")
        f = CubicSpline(self.x_values_given, self.y_values_given, bc_type='not-a-knot')
        #spline_extended = add_boundary_knots(f, self.x_values_given, self.y_values_given)
        y_extrapolated = f(x_axis_range)
        return x_axis_range, y_extrapolated


if __name__ == "__main__":

    path_data = './data/gl sensitivity template.csv'
    data = DataLoader(path_data)
    q_gl_list, q_fluid_wells_list = data.load_data_gl_template()
    q_gl_max = max([np.max(j) for j in q_gl_list])

    # interpolate
    q_gl_interpolated = []
    q_fluid_interpolated = []
    for i, j in zip(q_gl_list, q_fluid_wells_list):
        pchip = Interpolator(i, j, 100)
        result_pchip = pchip.pchip_interpolator()
        q_gl_interpolated.append(result_pchip[0])
        q_fluid_interpolated.append(result_pchip[1])

    for i,j in zip(q_gl_interpolated, q_fluid_interpolated):
        plt.plot(i,j)
    plt.title("Interpolation")
    plt.show()


    #extrapolate
    """q_gl_extrapolated = []
    q_fluid_extrapolated = []
    for i, j in zip(q_gl_interpolated, q_fluid_interpolated):
        ext = Extrapolator(i, j, 1, q_gl_max)
        result = ext.extrapolate_interp1d()
        q_gl_extrapolated.append(result[0])
        q_fluid_extrapolated.append(result[1])


    for i,j in zip(q_gl_extrapolated, q_fluid_extrapolated):
        plt.plot(i,j)
    plt.title("Extrapolation")
    plt.show()
    """

    x= q_gl_interpolated[0]
    y= q_fluid_interpolated[0]
    x_new = [0, 200,400,600,800,1000,1200,1400]
    print(x,y,x_new)

f = CubicSpline(x, y, bc_type='not-a-knot')
y_extrapolated = f(x_new)
print(y_extrapolated)
