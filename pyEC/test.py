"""
@Author: Jianchong Guo
@Time: 2023/11/27 14:50
"""
import numpy as np

from pyEC.problems.path_planning_problem.path_planning_problem import path_planning_problem
from pyEC.algorithms.path_planning_algorithm.NSGA_II import NSGA_II
import matplotlib.pyplot as plt

parameter = {'terrain': 8}
problem = path_planning_problem(n_population=100, n_objective=2, encoding_shape=(100, 3), max_function_evaluation=20000, parameter=parameter)
algorithm = NSGA_II()
algorithm.solve(problem)
# best  <Solutions>
best = algorithm.result[-1][1].best()

points = best.get_population_objective()

idx = np.argsort(points[:, 0])

points = points[idx]

# 提取 x 和 y 坐标
x = points[:, 0]
y = points[:, 1]

# 绘制连线
plt.plot(x, y, marker='o', linestyle='-')

# 设置图表标题和坐标轴标签
plt.title('Connected Points')
plt.xlabel('Length')
plt.ylabel('Threat')

# 显示图表
plt.show()


