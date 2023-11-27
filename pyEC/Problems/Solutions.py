"""
@Author: Jianchong Guo
@Time: 2023/11/25 21:47
"""

import numpy as np


class Solutions:
    """
    This is the class of solutions.
    An object of Solutions stores all the properties including decision variables,
    objective values, constraint violations, and additional properties of a solution.

    Solutions properties:
        population_encoding             <array>         decision variables of the solutions          (n_population, encoding_shape)
        population_objective            <array>         objective values of the solutions            (n_population, n_objective)
        population_constraint           <array>         constraint violations of the solutions       (b_population)
        additional_properties           <array>         additional properties of the solutions

    Solutions methods:
        Solutions                       the constructor setting all the properties of solutions
        get_population_encoding         get the array of decision variables of multiple solutions
        get_population_objective        get the array of objective values of multiple solutions
        get_population_constraint       get the array of constraint violations of multiple solutions
        get_additional_properties       get the array of additional properties of multiple solutions
    """

    def __init__(self, population_encoding, population_objective, population_constraint, additional_properties=None):
        self.population_encoding = population_encoding
        self.population_objective = population_objective
        self.population_constraint = population_constraint
        self.additional_properties = additional_properties if additional_properties is not None else np.array([])

    def get_population_encoding(self):
        return self.population_encoding

    def get_population_objective(self):
        return self.population_objective

    def get_population_constraint(self):
        return self.population_constraint

    def get_additional_properties(self):
        return self.additional_properties

    # def best(self):
    #     """
    #     Get the best solutions among multiple solutions.
    #     Returns the feasible and non-dominates solutions among multiple solutions.
    #     If the solutions have a single objective, the feasible solution with minimum
    #     objective value is returned.
    #     """
    #     feasible = np.all(self.constraint_violation <= 0, axis=1)
    #     if not any(feasible):
    #         return np.array([])
