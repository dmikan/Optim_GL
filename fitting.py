from data_loader import DataLoader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class Fitting():
    """Class implementing fitting of performance curves"""

    def __init__(self, q_gl, q_oil):
        self.q_gl = q_gl
        self.q_oil = q_oil

    def fit(self, model):
        params_list, _ = curve_fit(model, self.q_gl, self.q_oil)
        return params_list

    def model_namdar(self, q_gl_range, a, b, c, d, e):
        return (
            a + b * q_gl_range + c * (q_gl_range ** 0.7) +
            d * np.log(q_gl_range + 0.9) + e * np.exp(-(q_gl_range ** 0.6))
        )
    
    def model_dan(self, q_gl_range, a, b, c, d, e):
        return (
            a + b * q_gl_range + c * (q_gl_range ** 0.7) +
            d * np.log(q_gl_range + 1) + e * np.exp(-(q_gl_range ** 0.6))
    )

    def plot_fitting(self, q_gl_range, y_pred, well):
        plt.plot(q_gl_range, y_pred, label="Fitted curve")
        plt.scatter(self.q_gl, self.q_oil, color='red', label='Data points')
        plt.xlabel('q_gl')
        plt.ylabel('q_oil')
        plt.title(f'Well {well}')
        plt.legend()
        plt.grid()
        plt.show()

if __name__ == "__main__":
    # Cargar datos
    load = DataLoader('./data/gl_nishikiori_data_five.csv')
    q_gl_list, q_oil_list = load.load_data_gl_template()

    # Configurar la figura con 2 filas y 3 columnas, aumentando la altura
    fig, axes = plt.subplots(2, 3, figsize=(15, 12), constrained_layout=True)
    axes = axes.flatten()  # Para iterar fácilmente

    # Asegurar que todos los valores en q_gl_list sean numéricos
    q_gl_list = [[x for x in q_gl if not np.isnan(x)] for q_gl in q_gl_list]
    q_oil_list = [[x for x in q_oil if not np.isnan(x)] for q_oil in q_oil_list]

    # Ahora se puede calcular el máximo sin errores
    q_gl_max = max([np.max(j) for j in q_gl_list])
    q_gl_range = np.linspace(0, q_gl_max, 1000)

    # Crear un DataFrame con la primera columna como q_gl_range
    df_results = pd.DataFrame({"q_gl": q_gl_range})

    for well in range(len(q_oil_list)):
        q_gl = q_gl_list[well]
        q_oil = q_oil_list[well]

        # Ajuste del modelo
        fitter = Fitting(q_gl, q_oil)
        a, b, c, d, e = fitter.fit(fitter.model_namdar)
        
        # Predecir valores
        y_pred = fitter.model_namdar(q_gl_range, a, b, c, d, e)

        # Reemplazar valores negativos con 0 en lugar de eliminarlos
        y_pred[y_pred < 0] = 0

        # Agregar columna al DataFrame con el nombre "Well_X"
        df_results[f"well_{well}"] = y_pred

        # Graficar en el subplot correspondiente
        ax = axes[well]
        ax.plot(q_gl_range, y_pred, label="Fitted curve")
        ax.scatter(q_gl, q_oil, color='red', label='Data points')
        ax.set_xlabel('q_gl')
        ax.set_ylabel('q_oil')
        ax.set_title(f'Well {well+1}')
        ax.legend()
        ax.grid()
    plt.show()

# Guardar el DataFrame como CSV
# df_results.to_csv("./data/fitted_curves.csv", index=False)