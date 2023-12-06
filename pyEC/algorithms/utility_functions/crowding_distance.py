"""
@Author: Jianchong Guo
@Time: 2023/12/6 11:44
"""
import numpy as np
import warnings

from pyEC.problems.solutions import Solutions


def crowding_distance(population: Solutions, front=None):
    """
    Calculate the crowding distance of solutions front.
    Args:
        population:     <Solutions>     An object of Solutions stores encoding, objective values, constraint and so on
        front:          <list>          front[i] denotes the front number of the i-th solution, start from 1

    Returns:
        crowd_distance  <array>         the crowding distances of solutions

    Examples:
        crowd_distance = crowding_distance(population)
        calculates the crowding distances of solutions according to their objective values in population.
        crowd_distance = crowding_distance(population, front)
        calculates the crowding distances of solutions in each non-dominated front,
        where front if the front numbers of solutions.
    """
    population_objective = population.get_population_objective()
    n_population, n_objective = population_objective.shape

    if front is None:
        front = np.ones(n_population).tolist()

    crowd_distance = np.zeros(n_population)
    fronts = np.setdiff1d(np.unique(front), np.inf)

    for f in fronts:
        idx = np.where(front == f)[0]
        f_max = np.max(population_objective[idx, :], axis=0)
        f_min = np.min(population_objective[idx, :], axis=0)

        for i in range(n_objective):
            p = population_objective[idx, :]
            rank = np.argsort(population_objective[idx, i])
            crowd_distance[idx[rank[0]]] = np.inf
            crowd_distance[idx[rank[-1]]] = np.inf

            for j in range(1, len(idx) - 1):
                warnings.filterwarnings("ignore", category=RuntimeWarning)
                crowd_distance[idx[rank[j]]] += ((population_objective[idx[rank[j + 1]], i]) - (population_objective[idx[rank[j - 1]], i])) / (f_max[i] - f_min[i])

    return crowd_distance


if __name__ == "__main__":
    from pyEC.algorithms.utility_functions.non_dominated_sort import non_dominated_sort

    arr = np.array([
        (0.1, 0.6),
        (0.2, 0.5),
        (0.3, 0.4),
        (0.4, 0.3),
        (0.5, 0.2),
        (0.6, 0.1),
    ])
    population = Solutions(population_encoding=None, population_objective=arr, population_constraint=None)
    front = non_dominated_sort(population)
    print(front)
    cd = crowding_distance(population, front)
    print(cd)