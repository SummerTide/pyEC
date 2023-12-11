"""
@Author: Jianchong Guo
@Time: 2023/11/22 13:30
"""

import numpy as np

from pyEC.problems.problem import Problem


class ZDT1(Problem):
    def setting(self):
        self.n_objective = 2
        if self.encoding_shape is None:
            self.encoding_shape = (30,)
        self.lower = np.zeros(self.encoding_shape)
        self.upper = np.ones(self.encoding_shape)

    def calculate_objective(self, population_encoding):
        population_objective = np.zeros([self.n_population, self.n_objective])
        population_objective[:, 0] = population_encoding[:, 0]
        g = 1 + 9 * np.mean(population_encoding[:, 1:], axis=1)
        h = 1 - np.sqrt(population_objective[:, 0] / g)
        population_objective[:, 1] = g * h
        return population_objective

    def get_optimum(self, N):
        r = np.zeros([N, self.n_objective])
        r[:, 0] = np.linspace(0, 1, N)
        r[:, 1] = 1 - np.sqrt(r[:, 0])
        return r

    def get_pareto_front(self):
        r = self.get_optimum(100)
        return r
