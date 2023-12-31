"""
@Author: Jianchong Guo
@Time: 2023/11/27 16:29
"""
from pyEC.problems.solutions import Solutions


def operator_GA(problem, parent: Solutions):
    """
    Crossover and mutation operators of genetic algorithm.
    Uses genetic operators to generate offsprings from problem based on parent.
    If parent is an array of SOLUTION objects, then offspring is also an array of SOLUTION objects.

    Example:
        offspring = OperatorGA(problem, parent)
        offspring = OperatorGA(problem, parent,


    """
    offspring = problem.evaluation(parent.get_population_encoding())
    return offspring