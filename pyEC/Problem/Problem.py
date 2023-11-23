"""
@Author: Jianchong Guo
@Time: 2023/11/22 13:39
"""

import numpy as np


class Problem:
    """
    This is the superclass of problems.
    An object of PROBLEM stores all the setting of the problem.

    Problem properties:
    N                   <int>               population size
    M                   <int>               number of objective
    D                   <int>               number of decision variables
    maxFE               <int>               maximum number of function evaluations
    FE                  <int>               number of consumed funtion evaluations
    maxRuntime          <int>               maximum runtime (in second)
    encoding            <array>             encoding scheme of each decision variable
    lower               <array>             lower bound of each decision variable
    upper               <array>             upper bound of each decision variable
    optimum             <array>             optimal objective values of the problem
    PF                  <array>             image of the Pareto Front
    parameter           <dict>              other parameters of the problem

    Problem methods:



    """

    def __init__(self, N=100, maxFE=10000, FE=0):
        self.N = N
        self.maxFE = maxFE
        self.FE = FE
        self.M = None
        self.D = None
        self.maxRuntime = np.inf
        self.encoding = None
        self.lower = None
        self.upper = None
        self.optimum = None
        self.PF = None
        self.parameter = {}

    def setting(self):
        """
        Default settings of the problem.
        This function is expected to be implemented in each subclass of PROBLEM,
        which is usually called by the constructor.

        """
        pass

    def initialization(self):
        """
        Generate multiple initial solutions.
        This function is usually called at the beginning of algorithms.

        Example:
            population = Problem.initialization(N)
        """
        popDec = np.zeros([self.N, self.D])


if __name__ == '__main__':
    P = Problem(a=1, b=2, c=3)
    print()

