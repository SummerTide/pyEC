"""
@Author: Jianchong Guo
@Time: 2023/11/27 16:45
"""

import numpy as np

from pyEC.algorithms.utility_functions.non_dominated_sort import non_dominated_sort
from pyEC.algorithms.utility_functions.crowding_distance import crowding_distance
from pyEC.problems.solutions import Solutions


def environment_selection(population: Solutions, n_population):
    """
    The environment selection of NSGA-II.
    """
    # non-dominated sorting
    front, max_front = non_dominated_sort(population, n_population)
    next = front < max_front

    # calculate the crowding distance of each solution
    crowd_distance = crowding_distance(population, front)
    last = np.where(front == max_front)[0]
    rank = np.argsort(crowd_distance[last])
    # a = np.sum(next)
    # b = rank[:n_population - np.sum(next)]
    # c = last.tolist()
    next[last[rank[:n_population - np.sum(next)]]] = True

    population = population[next]
    front = front[next]
    crowd_distance = crowd_distance[next]

    return population, front, crowd_distance


# if __name__ == "__main__":
#     pop_enc = np.array([
#         (1, 1, 2),
#         (1, 3, 2),
#         (1, 1, 2),
#         (2, 1, 2),
#         (1, 1, 2),
#         (1, 7, 2),
#     ])
#     pop_obj = np.array([
#         (0.1, 0.6),
#         (0.2, 0.5),
#         (0.3, 0.4),
#         (0.4, 0.3),
#         (0.5, 0.2),
#         (0.6, 0.1),
#     ])
#     pop_cons = np.zeros(6)
#     population = Solutions(population_encoding=pop_enc, population_objective=pop_obj, population_constraint=pop_cons)
#     population, front, crowd_distance = environment_selection(population, 3)
