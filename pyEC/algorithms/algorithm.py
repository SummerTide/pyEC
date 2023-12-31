"""
@Author: Jianchong Guo
@Time: 2023/11/23 22:47
"""

import math
from time import time, strftime, localtime
import numpy as np
import os
import sys


class Algorithm:
    """
    This is the superclass of algorithm.
    An object of algorithms stores the settings of the algorithm
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
        save
    """

    def __init__(self, parameter=None, save=np.inf, output_function=None):
        if parameter is None:
            parameter = {}
        self.parameter = parameter
        self.save = save
        self.output_function = output_function if output_function is not None else self._default_output
        self.problem = None
        self.result = None
        self.metric = None
        self.start_time = None

    def _default_output(self, problem):
        """
        The default output function of algorithms.
        """
        print(f"{type(self).__name__} on {problem.n_objective}-objective {type(problem).__name__} ({problem.function_evaluation / problem.max_function_evaluation * 100: .2f}%), {self.metric['runtime']: .2f}s passed...")

    def solve(self, problem):
        """
        Use the algorithm to solve a problem.

        Args:
            problem: a problems object

        Examples:
            algorithms.solve(problems)
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
        This function is expected to be implemented in each subclass of algorithms,
        which is usually called by algorithms.solve.
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
            while algorithms.not_terminated(population):
                ...
        """
        self.metric['runtime'] = self.metric['runtime'] + time() - self.start_time
        self.start_time = time()
        if self.problem.max_runtime < np.inf:
            self.problem.max_function_evaluation = self.problem.function_evaluation * self.problem.max_runtime / \
                                                   self.metric['runtime']
        num = max(1, abs(self.save))  # number of populations to save
        if math.isinf(num):
            index = max(0, len(self.result))
        else:
            index = max(0, min(min(num, len(self.result)), math.ceil(
                num * self.problem.function_evaluation / self.problem.max_function_evaluation)) - 1)
        self.result.insert(index, [self.problem.function_evaluation, population])
        self.output_function(self.problem)
        not_finish = self.problem.function_evaluation < self.problem.max_function_evaluation
        assert not_finish, 'pyEC: Termination' ''
        self.start_time = time()
        return not_finish

    def save_log(self, i, path=None, log_path=None):
        np.set_printoptions(threshold=sys.maxsize, suppress=True)
        if log_path is None:
            time_now = strftime("%Y-%m-%d-%H-%M", localtime())
            if path is None:
                path = "./log/{}".format(time_now)
            else:
                path = path
            if not os.path.exists(path):
                os.makedirs(path)
            log_path = path + f"/{type(self).__name__}" + ".txt"
            log = open(log_path, 'a')
            log.write(f"{type(self).__name__} on {self.problem.n_objective}-objective {type(self.problem).__name__}" + '\n')
        else:
            log_path = log_path
            log = open(log_path, 'a')
        log.write(f"loop: {i}" + '\n')
        array = self.result[-1][1].best().get_population_encoding()
        log.write(str(array) + '\n')
        log.close()
        return path, log_path


# if __name__ == "__main__":
#     Algorithm = Algorithm()
