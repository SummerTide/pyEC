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
    n_population                <int>               population size
    n_objective                 <int>               number of objective
    TODO: Need to think about variable names
    decision_variables          <array>             decision variables of the solution (individual encoding)
    max_function_evaluation     <int>               maximum number of function evaluations
    function_evaluation         <int>               number of consumed funtion evaluations
    max_runtime                 <int>               maximum runtime (in second)
    lower                       <array>             lower bound of each decision variable
    upper                       <array>             upper bound of each decision variable
    optimum                     <array>             optimal objective values of the problem
    pareto_front                <array>             image of the Pareto Front
    parameter                   <dict>              other parameters of the problem

    Problem methods:



    """

    def __init__(self, n_population=100, n_objective=1, encoding_shape=None, max_function_evaluation=10000, max_runtime=np.inf, parameter={}):
        self.n_population = n_population
        self.n_objective = n_objective
        self.encoding_shape = encoding_shape
        self.max_function_evaluation = max_function_evaluation
        self.function_evaluation = 0
        self.max_runtime = max_runtime
        self.lower = None
        self.upper = None
        self.optimum = None
        self.pareto_front = None
        self.parameter = parameter

        self.setting()
        self.get_optimum(10000)
        self.get_pareto_front()

    def setting(self):
        """
        Default settings of the problem.
        This function is expected to be implemented in each subclass of PROBLEM,
        which is usually called by the constructor.
        """
        pass

    def get_optimum(self, N):
        """
        Generate the optimums of the problem, which returns N optimums of the problem.
        For multi-objective optimization problems, an optimum can a point on the pareto front.
        """
        if self.n_objective > 1:
            r = np.zeros([N, self.n_objective])
        else:
            r = np.zeros([N])
        return r

    def get_pareto_front(self):
        """
        Generate the image of pareto front.
        """
        r = np.array([])
        return r


    def initialization(self, decision_variables=None):
        """
        Generate multiple initial solutions.
        This function is usually called at the beginning of algorithms.

        Example:
            population = Problems.initialization(N)
        """
        if decision_variables is None:
            decision_variables = np.zeros((self.n_population, ) + self.encoding_shape)
        # population = self.evaluation(decision_variables)
        # return population

    def evaluation(self):
        """
        Evaluate multiple solutions.
        Returns:

        """

    def repair(self, ):
        pass

    def calculate_objective(self, ):
        pass

    def calculate_constraint(self, ):
        pass



if __name__ == '__main__':
    parameters = {
        'a': 1,
        'b': 2,
        'c': 3
    }
    n_population = 10
    n_objective = 2
    encoding_shape = (50, 3)
    P = Problem(n_population=n_population, n_objective=n_objective, encoding_shape=encoding_shape, parameter=parameters)
    P.initialization()


