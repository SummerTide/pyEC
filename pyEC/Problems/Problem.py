"""
@Author: Jianchong Guo
@Time: 2023/11/22 13:39
"""

import numpy as np

from .Solutions import Solutions


class Problem:
    """
    This is the superclass of problems.
    An object of PROBLEM stores all the setting of the problem.

    Problem properties:
        n_population                <int>               population size
        n_objective                 <int>               number of objective
        encoding_shape              <array>             the shape of the individual encoding
        max_function_evaluation     <int>               maximum number of function evaluations
        function_evaluation         <int>               number of consumed funtion evaluations
        max_runtime                 <int>               maximum runtime (in second)
        lower                       <array>             lower bound of each decision variable
        upper                       <array>             upper bound of each decision variable
        optimum                     <array>             optimal objective values of the problem
        pareto_front                <array>             image of the Pareto Front
        parameter                   <dict>              other parameters of the problem

    Problem methods:
        Problem                     the constructor setting all the properties specifies by used
        setting                     default setting of the problem
        initialization              generate initial solutions
        evaluation                  evaluate solutions
        repair                      repair invalid solutions
        calculate_objective         calculate the objective values of solutions
        calculate_constraint        calculate the constraint violations of solutions
        get_optimum                 generate the optimal objective values of the problem
        get_pareto_front            generate the image of the pareto front
    """

    def __init__(self, n_population=100, n_objective=1, encoding_shape=None, max_function_evaluation=10000,
                 max_runtime=np.inf, parameter=None):
        if parameter is None:
            parameter = {}
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

    def initialization(self, population_encoding=None):
        """
        Generate multiple initial solutions.
        This function is usually called at the beginning of algorithms.

        Example:
            population = Problems.initialization(N)
        """
        if population_encoding is None:
            population_encoding = np.random.uniform(self.lower, self.upper, size=(self.n_population,) + self.encoding_shape)
            # population_encoding = np.zeros((self.n_population,) + self.encoding_shape)
        population = self.evaluation(population_encoding)
        return population

    def evaluation(self, population_encoding, additional_properties=None):
        """
        Evaluate multiple solutions.
        Args:
            population_encoding: (n_population, encoding_shape)
            additional_properties: <array> additional properties of the solution
        """
        population_encoding = self.repair(population_encoding)
        population_objective = self.calculate_objective(population_encoding)
        population_constraint = self.calculate_constraint(population_encoding)
        population = Solutions(population_encoding, population_objective, population_constraint, additional_properties)
        self.function_evaluation = self.function_evaluation + population.get_population_encoding().shape[0]
        return population

    def repair(self, population_encoding):
        """
        Repair multiple invalid solutions.
        Args:
            population_encoding: (n_population, encoding_shape)
        Returns:
            population_encoding: (n_population, encoding_shape)
        """
        if self.lower is not None and self.upper is not None:
            population_encoding = np.clip(population_encoding, self.lower, self.upper)
        return population_encoding

    def calculate_objective(self, population_encoding):
        """
        Calculate the objective values of multiple solutions.
        Args:
            population_encoding: (n_population, encoding_shape)
        Returns:
            population_objective: (n_population, n_objective)
        """

        population_objective = np.zeros([self.n_population, self.n_objective])
        return population_objective

    def calculate_constraint(self, population_encoding):
        """
        Calculate the constraint violations of multiple solutions.
        Args:
            population_encoding: (n_population, encoding_shape)
        Returns:
            population_constraint: (n_population)
        """
        population_constraint = np.zeros([self.n_population])
        return population_constraint

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


if __name__ == '__main__':
    parameters = {
        'a': 1,
        'b': 2,
        'c': 3
    }
    P = Problem(n_population=100, n_objective=2, encoding_shape=(50, 3), parameter=parameters)
    pop = P.initialization()
    print(pop.get_population_encoding().shape)
