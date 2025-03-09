import csv

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """Carga los datos desde un CSV y los transforma en listas."""
        data = []
        with open(self.file_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir encabezado si lo tiene
            for row in reader:
                data.append([float(x) for x in row])  # Convertir a float si es numérico
        return data
