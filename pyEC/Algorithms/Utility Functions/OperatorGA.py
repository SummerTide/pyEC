"""
@Author: Jianchong Guo
@Time: 2023/11/23 19:54
"""

def OperatorGA(problem, parent, **kwargs):
    """
    Crossover and mutation operators of genetic algorithm.
    Uses genetic operators to generate offsprings from problem based on parent.
    If parent is an array of SOLUTION objects, then offspring is also an array of SOLUTION objects.

    Example:
        offspring = OperatorGA(problem, parent)
        offspring = OperatorGA(problem, parent,


    """
