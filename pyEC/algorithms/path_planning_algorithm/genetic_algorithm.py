"""
@Author: Jianchong Guo
@Time: 2023/12/11 20:24
"""
import numpy as np

from pyEC.problems.solutions import Solutions


def getetic_algorithm(problem, parent: Solutions):
    # Crossover
    length = parent.len() // 2
    parent = parent.get_population_encoding()
    parent_encoding_1 = parent[:length]
    parent_encoding_2 = parent[length:length * 2]
    offspring_encoding_shape = list(parent_encoding_1.shape)
    offspring_encoding_shape[0] = offspring_encoding_shape[0] * 2
    offspring_encoding = np.zeros(offspring_encoding_shape)

    idx = np.random.randint(int(offspring_encoding_shape[1]), size=(length,))

    mask = np.arange(offspring_encoding_shape[1]) < idx[:, None]

    offspring_encoding[:length] = np.where(mask[:, :, None], parent_encoding_1, parent_encoding_2)
    offspring_encoding[length:] = np.where(mask[:, :, None], parent_encoding_2, parent_encoding_1)

    # Mutation
    random_array = np.random.randint(-3, 4, size=(problem.n_population, list(problem.encoding_shape)[0], 2))

    for i in range(1, problem.encoding_shape[0] - 1):
        offspring_encoding[:, i, 0] += random_array[:, i, 0]
        offspring_encoding[:, i, 0] = np.clip(offspring_encoding[:, i, 0], problem.lower[0][0],
                                              problem.upper[0][0]).astype(np.int32)
        offspring_encoding[:, i, 1] += random_array[:, i, 1]
        offspring_encoding[:, i, 1] = np.clip(offspring_encoding[:, i, 1], problem.lower[0][0],
                                              problem.upper[0][0]).astype(np.int32)
        arr1 = offspring_encoding[:, i, 0].astype(np.int32)
        arr2 = offspring_encoding[:, i, 1].astype(np.int32)
        z = problem.environment[arr1, arr2] + problem.safe_distance
        offspring_encoding[:, i, 2] = z

    offspring = problem.evaluation(offspring_encoding)
    return offspring
