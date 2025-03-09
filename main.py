from data_loader import DataLoader
from optimization_model import OptimizationModel
import pandas as pd

# Ruta del archivo CSV
csv_file = "data/datos.csv"

# Cargar los datos
loader = DataLoader(csv_file)
qgl, q_fluid_wells = loader.load_data()

# Crear modelo de optimización
model = OptimizationModel(qgl, q_fluid_wells)

# Construir el modelo paso a paso
model.construir_modelo()
model.agregar_restricciones()

# Resolver el modelo
model.resolver()

# Obtener resultados
resultados = model.obtener_resultados()

# Guardar los resultados en un archivo
output_file = "results/output.txt"
with open(output_file, "w") as file:
    file.write("Resultados de optimización:\n")
    for i, res in enumerate(resultados):
        file.write(f"Well {i+1}: {res}\n")

print("Optimización completada. Resultado guardado en 'results/output.txt'.")
