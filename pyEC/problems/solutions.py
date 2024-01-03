"""
@Author: Jianchong Guo
@Time: 2023/11/25 21:47
"""

import numpy as np

from pyEC.algorithms.utility_functions.non_dominated_sort import non_dominated_sort


class Solutions:
    """
    This is the class of solutions.
    An object of Solutions stores all the properties including decision variables,
    objective values, constraint violations, and additional properties of a solution.

    Solutions properties:
        population_encoding       <array>    decision variables of the solutions          (n_population, encoding_shape)
        population_objective      <array>    objective values of the solutions            (n_population, n_objective)
        population_constraint     <array>    constraint violations of the solutions       (n_population)
        additional_properties     <array>    additional properties of the solutions

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

    def __getitem__(self, item):
        if np.any(self.additional_properties):
            additional_properties = self.additional_properties[item]
        else:
            additional_properties = np.array([])
        population = Solutions(self.population_encoding[item], self.population_objective[item],
                               self.population_constraint[item], additional_properties)
        return population

    def replace(self, item, offspring):
        self.population_encoding[item] = offspring.population_encoding
        self.population_objective[item] = offspring.population_objective
        self.population_constraint[item] = offspring.population_constraint
        if np.any(offspring.additional_properties):
            self.additional_properties[item] = offspring.additional_properties

    def merge(self, offspring: 'Solutions'):
        if np.any(self.additional_properties):
            additional_properties = np.concatenate((self.additional_properties, offspring.additional_properties),
                                                   axis=0)
        else:
            additional_properties = np.array([])
        population = Solutions(np.concatenate((self.population_encoding, offspring.population_encoding), axis=0),
                               np.concatenate((self.population_objective, offspring.population_objective), axis=0),
                               np.concatenate((self.population_constraint, offspring.population_constraint), axis=0),
                               additional_properties)
        return population

    def len(self):
        return self.population_encoding.shape[0]

    def get_population_encoding(self):
        return self.population_encoding

    def get_population_objective(self):
        return self.population_objective

    def get_population_constraint(self):
        return self.population_constraint

    def get_additional_properties(self):
        return self.additional_properties

    def best(self):
        """
        Get the best solutions among multiple solutions.
        Returns the feasible and non-dominates solutions among multiple solutions.
        If the solutions have a single objective, the feasible solution with minimum
        objective value is returned.
        """
        front, max_front = non_dominated_sort(self)
        front = front
        best = self[front == 1]
        return best
