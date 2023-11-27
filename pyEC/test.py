"""
@Author: Jianchong Guo
@Time: 2023/11/27 14:50
"""

from Problems.ZDT.ZDT1 import ZDT1

problem = ZDT1(n_population=100, n_objective=2, encoding_shape=(30, ))
population = problem.initialization()
print()
