"""
@Author: Jianchong Guo
@Time: 2023/12/12 19:34
"""
import numpy as np
import math


def normal_boundary_intersection(n_population, n_objective):
    H1 = 1
    while math.comb(H1 + n_objective, n_objective - 1) <= n_population:
        H1 += 1

    w = np.array([math.comb(i, n_objective - 1) for i in range(1, H1 + n_objective)]) - \
        np.tile(np.arange(0, n_objective - 1), (math.comb(H1 + n_objective - 1, n_objective - 1), 1)) - 1
    w = w[0].reshape(w.shape[0], 1)
    w = (np.concatenate([w, np.zeros(w.shape) + H1], axis=1) - np.concatenate([np.zeros(w.shape), w], axis=1)) / H1

    if H1 < n_objective:
        H2 = 0
        while math.comb(H1 + n_objective - 1, n_objective - 1) + \
                math.comb(H2 + n_objective, n_objective - 1) <= n_population:
            H2 += 1
        if H2 > 0:
            w2 = np.array([math.comb(i, n_objective - 1) for i in range(1, H2 + n_objective)]) - \
                 np.tile(np.arange(0, n_objective - 1), (math.comb(H2 + n_objective - 1, n_objective - 1), 1)) - 1
            w2 = w2[0].reshape(w2.shape[0], 1)
            w2 = (np.concatenate([w2, np.zeros(w.shape) + H2], axis=1) -
                  np.concatenate([np.zeros(w2.shape), w2], axis=1)) / H2
            w = np.concatenate([w, w2 / 2 + 1 / (2 * n_objective)])
    w = np.maximum(w, 1e-6)
    n_population = w.shape[0]
    return w, n_population


def ILD(n_population, n_objective):
    pass


def MUD(n_population, n_objective):
    pass


def grid(n_population, n_objective):
    pass


def Latin(n_population, n_objective):
    pass


def uniform_point(n_population, n_objective, method='normal_boundary_intersection'):
    """
    Generate a set of uniformly distributed points.

    w, n_population = uniform_point(n_population, n_objective)
    Returns approximately n_population uniformly distributed points with n_objective objectives on the unit hyperplane
    via the normal-boundary intersection method with two layers.
    Note that the number of sampled points may be slightly smaller than the predefined size n_population due to
    the need for uniformity.

    """
    if method == 'normal_boundary_intersection':
        return normal_boundary_intersection(n_population, n_objective)
    elif method == 'ILD':
        return ILD(n_population, n_objective)
    elif method == 'MUD':
        return MUD(n_population, n_objective)
    elif method == 'grid':
        return grid(n_population, n_objective)
    elif method == 'Latin':
        return Latin(n_population, n_objective)
    else:
        raise ValueError("Invalid method")


# if __name__ == "__main__":
#     uniform_point(100, 2)
