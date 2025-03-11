import pulp
from data_loader import DataLoader


class OptimizationModel:
    """Class representing the optimisation model"""

    def __init__(self, q_gl, q_fluid_wells, available_qgl_total):
        self.q_gl = q_gl
        self.q_fluid_wells = q_fluid_wells
        self.available_qgl_total = available_qgl_total
        #self.prob = pulp.LpProblem("Maximizar_Suma_Wells", pulp.LpMaximize)
        #self.y_wells = self.define_variables()
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
        variables = self.define_variables()
        self.prob += pulp.lpSum(
            variables[i][j] * self.q_fluid_wells[i][j]
            for i in range(len(self.q_fluid_wells))
            for j in range(len(self.q_gl))
        ), "Objective function"
        return self.prob

    def add_constraints(self):
        """Make sure that each well selects only one value of q_gl"""
        variables = self.define_variables()
        for index, col in enumerate(variables):
            self.prob += pulp.lpSum(col) == 1, f"Restriccion_Seleccion_Unica_{index}"
        self.prob += pulp.lpSum(
            variables[i][j] * self.q_gl[j]
            for j in range(len(self.q_gl))
            for i in range(len(self.q_fluid_wells))
        ) <= self.available_qgl_total, "constraint q_gl available"
        return self.prob


    def solve_prob(self):
        """Solve the optimisation problem"""
        self.prob.solve()


    def get_results(self):
        """Obtiene los valores óptimos de qgl para cada well."""
        return [
            next((self.q_gl[j] for j in range(len(q_gl)) if pulp.value(well_fluid[j]) == 1), None)
            for well_fluid in self.q_fluid_wells
        ]


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
    results = model.get_results()


    #resolve = model.resolver()


    print(results)
