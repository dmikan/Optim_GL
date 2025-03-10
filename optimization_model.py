import pulp
from data_loader import DataLoader


class OptimizationModel:
    """Clase que representa el modelo de optimización."""

    def __init__(self, q_gl, q_fluid_wells):
        self.q_gl = q_gl
        self.q_fluid_wells = q_fluid_wells
        #self.prob = pulp.LpProblem("Maximizar_Suma_Wells", pulp.LpMaximize)
        #self.y_wells = self.definir_variables()
        #self.construir_modelo()
        #self.agregar_restricciones()

    def define_optimisation_problem(self):
        self.prob = pulp.LpProblem("Maximizar_Suma_Wells", pulp.LpMaximize)


    def definir_variables(self):
        """Define las variables binarias para cada well y qgl."""
        return [
            [pulp.LpVariable(f'y{well_index}_{i}', cat='Binary') for i in range(len(self.q_gl))]
            for well_index in range(len(self.q_fluid_wells))
        ]

    def construir_modelo(self):
        """Define la función objetivo a maximizar."""
        variables = self.definir_variables()
        self.prob += pulp.lpSum(
            variables[i][j] * self.q_fluid_wells[i][j]
            for i in range(len(self.q_fluid_wells))
            for j in range(len(self.q_gl))
        ), "Funcion_Objetivo"
        return self.prob

    def agregar_restricciones(self):
        """Asegura que cada well seleccione exactamente un valor de qgl."""
        for index, col in enumerate(self.q_fluid_wells):
            self.prob += pulp.lpSum(col) == 1, f"Restriccion_Seleccion_Unica_{index}"
        self.prob += pulp.lpSum(
            variables[i][j] * self.q_gl[j]
            for i in range(len(self.q_fluid_wells))
            for j in range(len(self.q_gl))
        ) <= 4000, "constraint q_gl available"
        print(prob)


    def resolver(self):
        """Resuelve el problema de optimización."""
        self.prob.solve()

    def obtener_resultados(self):
        """Obtiene los valores óptimos de qgl para cada well."""
        return [
            next((self.qgl[j] for j in range(len(y_well)) if pulp.value(y_well[j]) == 1), None)
            for y_well in self.y_wells
        ]


if __name__ == "__main__":
    path_data = './data/datos.csv'
    data = DataLoader(path_data)
    q_gl,q_fluid_wells = data.load_data()
    model = OptimizationModel(q_gl, q_fluid_wells)
    prob = model.define_optimisation_problem()
    variables = model.definir_variables()
    modelo = model.construir_modelo()
    restricciones = model.agregar_restricciones()
    #resolve = model.resolver()


    print(modelo)
    #print(len(q_fluid_wells))
