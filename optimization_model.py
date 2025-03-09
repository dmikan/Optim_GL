import pulp

class OptimizationModel:
    """Clase que representa el modelo de optimización."""

    def __init__(self, qgl, wells):
        self.qgl = qgl
        self.wells = wells
        self.prob = pulp.LpProblem("Maximizar_Suma_Wells", pulp.LpMaximize)
        self.y_wells = self.definir_variables()
        self.construir_modelo()
        self.agregar_restricciones()

    def definir_variables(self):
        """Define las variables binarias para cada well y qgl."""
        return [
            [pulp.LpVariable(f'y{well_index}_{i}', cat='Binary') for i in range(len(self.qgl))]
            for well_index in range(len(self.wells))
        ]

    def construir_modelo(self):
        """Define la función objetivo a maximizar."""
        self.prob += pulp.lpSum(
            self.y_wells[i][j] * self.wells[i][j]
            for i in range(len(self.wells))
            for j in range(len(self.qgl))
        ), "Funcion_Objetivo"

    def agregar_restricciones(self):
        """Asegura que cada well seleccione exactamente un valor de qgl."""
        for i, y_well in enumerate(self.y_wells):
            self.prob += pulp.lpSum(y_well) == 1, f"Restriccion_Seleccion_Unica_{i}"

    def resolver(self):
        """Resuelve el problema de optimización."""
        self.prob.solve()

    def obtener_resultados(self):
        """Obtiene los valores óptimos de qgl para cada well."""
        return [
            next((self.qgl[j] for j in range(len(y_well)) if pulp.value(y_well[j]) == 1), None)
            for y_well in self.y_wells
        ]
