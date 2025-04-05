from data_loader import DataLoader
from optimization_model import OptimizationModel
import pandas as pd
import numpy as np
from fitting import Fitting
import matplotlib.pyplot as plt

# Cargar los datos
csv_file = "./data/gl_nishikiori_data_five.csv"
loader = DataLoader(csv_file)
q_gl_list, q_oil_list = loader.load_data_gl_template()

# Generar valores escalados para graficar
q_gl_max = max([np.max(j) for j in q_gl_list])
q_gl_range = np.linspace(0, q_gl_max, 1000)

y_pred_list = []
# Crear un DataFrame con la primera columna como q_gl_range
for well in range(len(q_oil_list)):
    q_gl = q_gl_list[well]
    q_oil = q_oil_list[well]

    # Ajuste del modelo
    fitter = Fitting(q_gl, q_oil)
    y_pred = fitter.fit(model = fitter.model_namdar,
                        range = q_gl_range)
    y_pred_list.append(y_pred)

# Crear modelo de optimización
model = OptimizationModel(q_gl = q_gl_range, 
                          q_fluid_wells = y_pred_list, 
                          available_qgl_total = 4600)

# Construir el modelo paso a paso
model.define_optimisation_problem()
model.define_variables()
model.build_objective_function()
model.add_constraints()

# Resolver el problema de optimización
model.solve_prob()

# Obtener resultados
result_prod_rates = model.get_maximised_prod_rates()
result_optimal_qgl = model.get_optimal_injection_rates()
results = list(zip(result_prod_rates, result_optimal_qgl))

# Definir el archivo de salida
output_file = "results/output.txt"

# Escribir los resultados en el archivo
with open(output_file, "w") as file:
    file.write("=== Resultados de Optimización ===\n\n")

    # Producción y q_gl óptimos
    file.write(f"Producción total: {sum(result_prod_rates)}\n\n")
    file.write(f"Valor total óptimo de q_gl: {sum(result_optimal_qgl)}\n\n")

    # Resultados por pozo
    file.write("Resultados por pozo:\n")
    for i, (prod, qgl) in enumerate(results):
        file.write(f"Well {i+1}: Producción óptima = {prod}, q_gl óptimo = {qgl}\n")

print(f"Optimización completada. Resultado guardado en '{output_file}'.")


