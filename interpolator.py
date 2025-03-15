from data_loader import DataLoader
from scipy import interpolate
from scipy.interpolate import CubicSpline, PchipInterpolator, UnivariateSpline
import numpy as np
import pandas as pd
import matplotlib .pyplot as plt








if __name__ == "__main__":
    path_data = './data/datos.csv'
    data = DataLoader(path_data)
    q_gl,q_fluid_wells = data.load_data()
    # print(q_gl)
    # print(q_fluid_wells)
    df = pd.DataFrame(q_fluid_wells)
    df = df.transpose()
    # print(df)
    well1 = df[1]
    max_value_axis = max(q_gl)

    #well1_interp = well1.interpolate(method='polynomial', order=2, inplace=True, limit_direction='both')
    #spl = CubicSpline(q_gl, well1)
    #spl = PchipInterpolator(q_gl, well1)
    #spl = UnivariateSpline(q_gl, well1, s=10)


    injection_rates_range = np.arange(0,max_value_axis,10)
    print(injection_rates_range)
    linterp = np.interp(injection_rates_range, q_gl, well1)
    #interpolated_prod_rates = np.round(spl(injection_rates_range),0)

    #print(linterp)


    #plt.plot(q_gl, well1, 'o', color= 'red')
    plt.plot(injection_rates_range, linterp)
    plt.show()
