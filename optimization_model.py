import pulp
from data_loader import DataLoader


class OptimizationModel:
    """Class representing the optimisation model"""

    def __init__(self, q_gl, q_fluid_wells, available_qgl_total):
        self.q_gl = q_gl
        self.q_fluid_wells = q_fluid_wells
        self.available_qgl_total = available_qgl_total
        #self.prob = pulp.LpProblem("Maximizar_Suma_Wells", pulp.LpMaximize)
        self.variables = self.define_variables()
        #self.build_objective_function()
        #self.agregar_restricciones()

    def define_optimisation_problem(self):
        self.prob = pulp.LpProblem("Maximise the sum of wells' production", pulp.LpMaximize)


    def define_variables(self):
        """Define the binary variables for each q_gl and q_fluid"""
        binary_variables = [
            [pulp.LpVariable(f'y{well_index}_{i}', cat='Binary') for i in range(len(self.q_gl))]
            for well_index in range(len(self.q_fluid_wells))
        ]
        return binary_variables

    def build_objective_function(self):
        """Defines the objective function to be maximised"""
        self.prob += pulp.lpSum(
            self.variables[i][j] * self.q_fluid_wells[i][j]
            for i in range(len(self.q_fluid_wells))
            for j in range(len(self.q_gl))
        ), "Objective function"
        #return self.prob

    def add_constraints(self):
        """Make sure that each well selects only one value of q_gl"""
        for index, col in enumerate(self.variables):
            self.prob += pulp.lpSum(col) == 1, f"Restriccion_Seleccion_Unica_{index}"
        self.prob += pulp.lpSum(
            self.variables[i][j] * self.q_gl[j]
            for j in range(len(self.q_gl))
            for i in range(len(self.q_fluid_wells))
        ) <= self.available_qgl_total, "constraint q_gl available"
        #return self.prob


    def solve_prob(self):
        """Solve the optimisation problem"""
        self.prob.solve()
        #return self.prob


    def get_results(self):
        """Obtiene los valores óptimos de qgl para cada well."""
        return [
            next((self.q_gl[j] for j in range(len(self.q_gl)) if pulp.value(well_fluid[j]) == 1), None)
            for well_fluid in self.q_fluid_wells
        ]

    def test(self):
        well1 = pulp.lpSum(self.variables[0][i] * self.q_fluid_wells[0][i] for i in range(len(self.q_gl)))
        #pulp.value(well1)
        well2 = pulp.lpSum(self.variables[1][i] * self.q_fluid_wells[1][i] for i in range(len(self.q_gl)))
        #pulp.value(well2)
        well3 = pulp.lpSum(self.variables[2][i] * self.q_fluid_wells[2][i] for i in range(len(self.q_gl)))
        #pulp.value(well3)
        well4 = pulp.lpSum(self.variables[3][i] * self.q_fluid_wells[3][i] for i in range(len(self.q_gl)))
        #pulp.value(well4)
        print("RESULTADOS")
        return [pulp.value(well1), pulp.value(well2), pulp.value(well3), pulp.value(well4)]




if __name__ == "__main__":
    path_data = './data/datos.csv'
    data = DataLoader(path_data)
    q_gl,q_fluid_wells = data.load_data()
    model = OptimizationModel(q_gl, q_fluid_wells, 4000)
    (model.define_optimisation_problem())
    model.define_variables()
    model.build_objective_function()
    model.add_constraints()
    model.solve_prob()
    #results = model.get_results()


    #resolve = model.resolver()


    print(model.test())
