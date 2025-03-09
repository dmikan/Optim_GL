from data_loader import DataLoader
from optimization_model import OptimizationModel

# Ruta del archivo CSV
csv_file = "data/datos.csv"

# Cargar los datos
loader = DataLoader(csv_file)
data = loader.load_data()

# Extraer qgl y wells del dataset
qgl = data[0]  # Primera fila es qgl
wells = data[1:]  # Resto de filas son los wells

# Crear modelo de optimización
model = OptimizationModel(qgl, wells)

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
