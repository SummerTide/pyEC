"""
@Author: Jianchong Guo
@Time: 2023/11/23 22:47
"""



class Algorithm:
    """
    This is the superclass of algorithm.
    An object of Algorithm stores the settings of the algorithm
    and the data generated in current execution.

    Algorithm properties:
    parameter           <dict>              parameters of the algorithm
    save                <int>               number of populations saved in an execution
    outputFunction      <function>          function called after each generation
    problem             <class>             problem solved in current execution
    result              <list>              populations saved in current execution
    metric              <dict>              metric values of current populations

    Algorithm methods:

    """
    def __init__(self):
        self.parameter = {}
        self.save = -10
        self.outputFunction = self._default_output
        self.problem = None
        self.result = []
        self.metric = {}

    def _default_output(self, Problem):
        # TODO:
        pass