"""
@Author: Jianchong Guo
@Time: 2023/11/23 22:47
"""

import math
from time import time
import numpy as np


class Algorithm:
    """
    This is the superclass of algorithm.
    An object of Algorithms stores the settings of the algorithm
    and the data generated in current execution.

    Algorithm properties:
        parameter           <dict>              parameters of the algorithm
        save                <int>               number of populations saved in an execution
        output_function     <function>          function called after each generation
        problem             <class>             problem solved in current execution
        result              <list>              populations saved in current execution
        metric              <dict>              metric values of current populations

    Algorithm methods:
        Algorithm           the constructor setting all the properties specified by user
        solve               use the algorithm to solve a problem
        main                the main function of the algorithm
        not_terminated      the function called after each generation of the execution
    """

    def __init__(self, parameter={}, save=-10, output_function=None):
        self.parameter = parameter
        self.save = save
        self.output_function = output_function if output_function is not None else self._default_output
        self.problem = None
        self.result = None
        self.metric = None
        self.start_time = None

    def _default_output(self, problem):
        """
        The default output function of Algorithms.
        """
        print(
            f"{type(self).__name__} on {problem.n_objective}-objective {type(problem).__name__} ({problem.function_evaluation / problem.max_function_evaluation * 100: .2f}%), {self.metric['runtime']: .2f}s passed...")

    def solve(self, problem):
        """
        Use the algorithm to solve a problem.

        Args:
            problem: a Problems object

        Examples:
            Algorithms.solve(Problems)
        """
        try:
            self.result = []
            self.metric = {'runtime': 0}
            self.problem = problem
            self.problem.function_evaluation = 0
            self.start_time = time()
            self.main(problem)
        except Exception as err:
            if str(err) != 'pyEC: Termination':
                raise err

    def main(self, problem):
        """
        The main function of the algorithm.
        This function is expected to be implemented in each subclass of Algorithms,
        which is usually called by Algorithms.solve.
        """
        pass

    def not_terminated(self, population):
        """
        The function called after each generation of the execution.
        self.not_terminated(population) stores the population as the result
        of the current execution, and returns True if the algorithm should
        be terminated, i.e., the number of function evaluations or runtime exceeds.

        self.output_function is called here, whose runtime will not be counted
        in the runtime of current execution.

        Returns:
            not_finish       <bool>      True if the algorithm should not be terminated

        Examples:
            while Algorithms.not_terminated(population):
                ...
        """
        self.metric['runtime'] = self.metric['runtime'] + time() - self.start_time
        self.start_time = time()
        if self.problem.max_runtime < np.inf:
            self.problem.max_function_evaluation = self.problem.function_evaluation * self.problem.max_runtime / \
                                                   self.metric['runtime']
        num = max(1, abs(self.save))  # number of populations to save
        index = max(0, min(min(num, len(self.result)), math.ceil(
            num * self.problem.function_evaluation / self.problem.max_function_evaluation)) - 1)
        self.result[index] = [self.problem.function_evaluation, population]
        self.output_function(self.problem)
        not_finish = self.problem.function_evaluation < self.problem.max_function_evaluation
        assert not_finish, 'pyEC: Termination' ''
        self.start_time = time()
        return not_finish


if __name__ == "__main__":
    Algorithm = Algorithm()
