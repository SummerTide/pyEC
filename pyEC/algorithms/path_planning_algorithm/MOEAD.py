"""
@Author: Jianchong Guo
@Time: 2023/12/12 20:25
"""
import numpy as np

from pyEC.algorithms.algorithm import Algorithm
from pyEC.algorithms.utility_functions.uniform_point import uniform_point
from pyEC.algorithms.path_planning_algorithm.genetic_algorithm import getetic_algorithm


class MOEAD(Algorithm):
    def main(self, problem):
        # Parameter setting
        type = self.parameter['type']

        # Generate the weight vectors
        w, problem.n_population = uniform_point(problem.n_population, problem.n_objective)
        T = np.ceil(problem.n_population / 10).astype(int)

        # Detect the neighbors of each solution
        B = np.linalg.norm(w - w[:, np.newaxis], axis=2)
        B = np.argsort(B, axis=1)
        B = B[:, :T]

        # Generate random population
        population = problem.initialization()
        Z = np.min(population.get_population_objective(), axis=0)

        # Optimization
        while self.not_terminated(population):
            # For each solution
            for i in range(problem.n_population):
                # Choose the parents
                P = B[i, np.random.permutation(T)]
                # P = np.array([8,5,9,1,0,4,7,3,6,2])

                pool = P[0:2]
                # Generate an offspring
                offspring = getetic_algorithm(problem, population[pool])

                # Update the ideal point
                Z = np.minimum(Z, offspring[0:1].get_population_objective())
                # Z = np.array([0.0119, 2.4358])

                # Update the neighbors
                if type == 1:
                    # PBI approach
                    normW = np.linalg.norm(w[P, :], axis=1)
                    normP = np.linalg.norm(population[P].get_population_objective() - np.tile(Z, (T, 1)), axis=1)
                    normO = np.linalg.norm(offspring.get_population_objective() - Z)
                    CosineP = np.sum((population[P].get_population_objective() - np.tile(Z, (T, 1))) * w[P, :],
                                     axis=1) / (normW * normP)
                    CosineO = np.sum((np.tile(offspring.get_population_objective() - Z, (T, 1)) * w[P, :]), axis=1) / (
                                normW * normO)
                    g_old = normP * CosineP + 5 * normP * np.sqrt(1 - CosineP ** 2)
                    g_new = normO * CosineO + 5 * normO * np.sqrt(1 - CosineO ** 2)
                elif type == 2:
                    # Tchebycheff approach
                    # Checked
                    g_old = np.max(np.abs(population[P].get_population_objective() - np.tile(Z, (T, 1))) * w[P, :],
                                   axis=1)
                    g_new = np.max(np.tile(np.abs(offspring.get_population_objective() - Z), (T, 1)) * w[P, :], axis=1)
                elif type == 3:
                    # Tchebycheff approach with normalization
                    Zmax = np.max(population.get_population_objective(), axis=0)
                    g_old = np.max(
                        np.abs(population[P].get_population_objective() - np.tile(Z, (T, 1))) / np.tile(Zmax - Z,
                                                                                                        (T, 1)) * w[P,
                                                                                                                  :],
                        axis=1)
                    g_new = np.max(
                        np.tile(np.abs(offspring[0:1].get_population_objective() - Z) / (Zmax - Z), (T, 1)) * w[P, :],
                        axis=1)
                elif type == 4:
                    # Modified Tchebycheff approach
                    g_old = np.max(np.abs(population[P].get_population_objective() - np.tile(Z, (T, 1))) / w[P, :],
                                   axis=1)
                    g_new = np.max(np.tile(np.abs(offspring.get_population_objective() - Z), (T, 1)) / w[P, :], axis=1)
                else:
                    raise ValueError("Invalid type")

                idx = P[g_old >= g_new]
                population.replace(idx, offspring[0:1])

                Z = np.minimum(Z, offspring[1:2].get_population_objective())

                if type == 3:
                    Zmax = np.max(population.get_population_objective(), axis=0)
                    g_old = np.max(
                        np.abs(population[P].get_population_objective() - np.tile(Z, (T, 1))) / np.tile(Zmax - Z,
                                                                                                        (T, 1)) * w[P,
                                                                                                                  :],
                        axis=1)
                    g_new = np.max(
                        np.tile(np.abs(offspring[1:2].get_population_objective() - Z) / (Zmax - Z), (T, 1)) * w[P, :],
                        axis=1)

                idx = P[g_old >= g_new]
                population.replace(idx, offspring[1:2])



