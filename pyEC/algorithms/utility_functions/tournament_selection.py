"""
@Author: Jianchong Guo
@Time: 2023/12/6 15:45
"""
import numpy as np


def tournament_selection(k, n_population, *args):
    """
    Tournament selections, which returns the indices of n-population solutions by k-tournament selection based on their
    fitness values. In each selection, the candidate having the minimum fitness1 value will be selected: if multiple
    candidates have the same minimum value of fitness1, then the one with the smallest fitness2 value is selected, and
    so on.
    Args:
        k:
        n_population:
        *args:

    Returns:

    """
    args_flat = [np.reshape(arg, (-1, 1)) for arg in args]
    fitness, location = np.unique(np.hstack(args_flat), axis=0, return_inverse=True)
    rank = np.lexsort(fitness.T[:-1, :])
    rank = np.argsort(rank)

    parents = np.random.randint(len(args[0] - 1), size=(k, n_population))
    best = np.argmin(rank[location[parents]], axis=0)
    selected_location = parents[best, np.arange(n_population)]

    return selected_location


# if __name__ == "__main__":
#     front = np.array([2, 1, 2, 1, 1, 1, 1, 1, 1, 3])
#     crowd_distance = np.array([np.inf, 1.184, np.inf, 0.9229, 1.0306, np.inf, np.inf, np.inf, np.inf, np.inf,])
#     mating_pool = tournament_selection(2, 10, front, -crowd_distance)
