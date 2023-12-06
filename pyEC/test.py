"""
@Author: Jianchong Guo
@Time: 2023/11/27 14:50
"""

from pyEC.problems.ZDT.ZDT1 import ZDT1
from pyEC.algorithms.NSGA_II.NSGA_II import NSGA_II

problem = ZDT1(n_population=100, n_objective=2, encoding_shape=(30, ))
# population = problem.initialization()
algorithm = NSGA_II()
algorithm.solve(problem)

