"""
@Author: Jianchong Guo
@Time: 2023/11/27 16:45
"""

from pyEC.algorithms.algorithm import Algorithm
from pyEC.algorithms.NSGA_II.environmental_selection import environment_selection
from pyEC.algorithms.utility_functions.tournament_selection import tournament_selection
from pyEC.algorithms.utility_functions.operator_GA import operator_GA


class NSGA_II(Algorithm):
    def main(self, problem):
        population = problem.initialization()
        population, front, crowd_distance = environment_selection(population, problem.n_population)

        while self.not_terminated(population):
            mating_pool = tournament_selection(2, problem.n_population, front, -crowd_distance)
            offspring = operator_GA(problem, population[mating_pool])
            population, front, crowd_distance = environment_selection(population.merge(offspring), problem.n_population)
