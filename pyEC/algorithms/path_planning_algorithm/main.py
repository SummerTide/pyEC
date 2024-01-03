"""
@Author: Jianchong Guo
@Time: 2023/12/25 10:51
"""
import numpy as np

from pyEC.problems.path_planning_problem.path_planning_problem import path_planning_problem
from pyEC.algorithms.path_planning_algorithm.NSGA_II import NSGA_II
from pyEC.algorithms.path_planning_algorithm.MOEAD import MOEAD
import matplotlib.pyplot as plt


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
import math

if __name__ == "__main__":
    parameter = {'terrain': 8}
    max_loop = 5
    n_population = 100
    encoding_shape = (100, 3)
    max_function_evaluation = 20000
    path = None
    log_path_NSGA_II = None
    log_path_MOEAD = None

    for i in range(max_loop):
        algorithm_NSGA_II = NSGA_II()
        parameter_algorithm = {'type': 3}
        algorithm_MOEAD = MOEAD(parameter=parameter_algorithm)

        problem_NSGA_II = path_planning_problem(n_population=n_population, n_objective=2, encoding_shape=encoding_shape,
                                                max_function_evaluation=max_function_evaluation, parameter=parameter)
        problem_MOEAD = path_planning_problem(n_population=n_population, n_objective=2, encoding_shape=encoding_shape,
                                              max_function_evaluation=max_function_evaluation, parameter=parameter)

        algorithm_NSGA_II.solve(problem_NSGA_II)
        path, log_path_NSGA_II = algorithm_NSGA_II.save_log(i, path, log_path_NSGA_II)

        algorithm_MOEAD.solve(problem_MOEAD)
        path, log_path_MOEAD = algorithm_MOEAD.save_log(i, path, log_path_MOEAD)

        # Save PF
        best_NSGA_II = algorithm_NSGA_II.result[-1][1].best()
        points_NSGA_II = best_NSGA_II.get_population_objective()
        idx_NSGA_II = np.argsort(points_NSGA_II[:, 0])
        points_NSGA_II = points_NSGA_II[idx_NSGA_II]

        best_MOEAD = algorithm_MOEAD.result[-1][1].best()
        points_MOEAD = best_MOEAD.get_population_objective()
        idx_MOEAD = np.argsort(points_MOEAD[:, 0])
        points_MOEAD = points_MOEAD[idx_MOEAD]

        # 绘制连线
        plt.plot(points_NSGA_II[:, 0], points_NSGA_II[:, 1], "o--", label="NSGA_II")
        plt.plot(points_MOEAD[:, 0], points_MOEAD[:, 1], "D--", label="MOEAD")
        plt.legend()

        # 设置图表标题和坐标轴标签
        plt.title('Pareto Front')
        plt.xlabel('Length/m')
        plt.ylabel('Threat/#')

        # 显示图表
        plt.savefig(f"./img/Path_{i}_pareto.png")
        plt.cla()
        plt.clf()
        plt.close()

        # for j in range(best.len()):
        #     smooth_line = best[j].get_population_encoding()
        #
        #     terrain = problem_NSGA_II.terrain
        #     z = terrain
        #     x_max = z.shape[0]
        #     y_max = z.shape[1]
        #     z_max = np.max(z)
        #     z_max = math.ceil((z_max / 500.0) + 0.001) * 500
        #     x = np.linspace(0, x_max - 1, x_max)
        #     y = np.linspace(0, y_max - 1, y_max)
        #     x, y = np.meshgrid(x, y)
        #
        #     fig = plt.figure()
        #     ax = fig.add_subplot(111, projection='3d')
        #
        #     surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='jet', edgecolor='None', vmin=0, vmax=z_max)
        #
        #     for k in range(1, smooth_line.shape[0]):
        #         xs = smooth_line[k - 1][0], smooth_line[k][0]
        #         ys = smooth_line[k - 1][1], smooth_line[k][1]
        #         zs = smooth_line[k - 1][2], smooth_line[k][2]
        #         ax.plot3D(xs, ys, zs, color='r', alpha=1)
        #
        #     ax.set_zlim([0, z_max + 500])
        #
        #     ax.set_xlabel('X/km').set_fontname('Times New Roman')
        #     ax.set_ylabel('Y/km', rotation=90).set_fontname('Times New Roman')
        #     # ax.set_zlabel('Z/m').set_fontname('Times New Roman')
        #
        #     ax.xaxis.set_major_locator(MultipleLocator(100))
        #     ax.yaxis.set_major_locator(MultipleLocator(100))
        #     ax.zaxis.set_ticks([])
        #     # ax.axis('off')
        #
        #     plt.xticks(fontsize=8)
        #     plt.yticks(fontsize=8)
        #
        #     fig.colorbar(surf, ax=ax, orientation='vertical', pad=0.1)
        #
        #     ax.view_init(elev=90, azim=-90)
        #     plt.savefig(f"./img/Path_{i}_{j}.png")
        #     plt.cla()
        #     plt.clf()
        #     plt.close()
