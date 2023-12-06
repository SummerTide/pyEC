"""
@Author: Jianchong Guo
@Time: 2023/11/27 16:46
"""
from pyEC.problems.solutions import Solutions
import numpy as np


def non_dominated_sort(population: Solutions, n_sort=np.inf):
    """
    Perform non-dominated sorting by using efficient non-dominated sort.
    Args:
        population:     <Solutions>      An object of Solutions stores encoding, objective values, constraint and so on
        n_sort:         <int>            the number of solutions to be sorted as least

    Returns:
        front           <list>           front[i] denotes the front number of the i-th solution, start from 1

    Examples:
        front_no, max_front_no = non_dominated_sort(population, 5)
    """
    population_objective = population.get_population_objective()
    # n_population, n_objective = population_objective.shape

    front = ENS_SS(population_objective, n_sort)

    # TODO: Implement tree-based efficient non-dominated sort (T_ENS)
    # if n_population < 500 or n_objective < 3:
    #     front = ENS_SS(population_objective, n_sort)
    # else:
    #     front = T_ENS(population_objective, n_sort)

    return front


def ENS_SS(population_objective, n_sort):
    population_objective, location = np.unique(population_objective, axis=0, return_inverse=True)
    table = np.histogram(location, bins=np.arange(0, max(location) + 2))[0]
    # table     <array>     if location = [0 0 1 1 1], table = [2 3]
    n_population, n_objective = population_objective.shape
    front = np.full(n_population, np.inf)
    max_front = 0

    while np.sum(table[front < np.inf]) < min(n_sort, len(location)):
        max_front += 1
        for i in range(n_population):
            if front[i] == np.inf:
                dominated = False
                for j in range(i - 1, -1, -1):
                    if front[j] == max_front:
                        n = 1
                        while n < n_objective and population_objective[i][n] >= population_objective[j][n]:
                            n += 1
                        dominated = n >= n_objective
                        if dominated or n_objective == 1:
                            break
                if not dominated:
                    front[i] = max_front

    front = front[location]
    return front


def T_ENS(population_objective, n_sort):
    pass


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    arr = np.array([
        (0.1, 0.1),
        (0.2, 0.2),
        (0.3, 0.3),
        (0.4, 0.4),
        (0.5, 0.5),
        (0.6, 0.6),
    ])
    f = ENS_SS(arr, 10)
    print(f)
    plt.scatter(arr[:, 0], arr[:, 1], label='All Points')

    # 添加标签和标题
    plt.xlabel('Objective 1')
    plt.ylabel('Objective 2')
    plt.title('Pareto Front Example')

    # 添加图例
    plt.legend()

    # 显示图形
    plt.show()
