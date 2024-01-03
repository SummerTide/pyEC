"""
@Author: Jianchong Guo
@Time: 2023/12/8 16:50
"""

import numpy as np

from pyEC.problems.problem import Problem
from pyEC.problems.path_planning_problem.simulated_digital_terrain import terrain_three, terrain_four, terrain_eight


class path_planning_problem(Problem):
    def __init__(self, n_population=20, n_objective=2, encoding_shape=(100, 3), max_function_evaluation=4000, parameter=None):
        if parameter.get('terrain') is None:
            self.terrain = terrain_three()
        elif parameter['terrain'] == 3:
            self.terrain = terrain_three()
        elif parameter['terrain'] == 4:
            self.terrain = terrain_four()
        elif parameter['terrain'] == 8:
            self.terrain = terrain_eight()
        else:
            raise ValueError("Invalid terrain")
        self.start = (0, 0)
        self.destination = (199, 199)
        self.safe_distance = 200
        super().__init__(n_population=n_population, n_objective=n_objective, encoding_shape=encoding_shape,
                         max_function_evaluation=max_function_evaluation, parameter=parameter)

    def setting(self):
        self.lower = np.zeros(self.encoding_shape)
        self.upper = np.ones(self.encoding_shape) * (self.terrain.shape[0] - 1)
        self.upper[:, 2] = np.inf

    def initialization(self, population_encoding=None):
        if population_encoding is None:
            population_encoding = np.zeros((self.n_population,) + self.encoding_shape)

            x = (self.destination[0] - self.start[0]) / (self.encoding_shape[0] - 1)
            y = (self.destination[1] - self.start[1]) / (self.encoding_shape[0] - 1)

            random_array = np.random.randint(-1, 2, size=(self.n_population, list(self.encoding_shape)[0], 2))
            mutation_probability = 0.2
            zero_array = np.random.choice([0, 1],
                                          size=(self.n_population, list(self.encoding_shape)[0], 2),
                                          p=[mutation_probability, 1 - mutation_probability])
            random_array = random_array * zero_array
            random_array[0, :, :] = 0

            population_encoding[:, 0, 0] = self.start[0]
            population_encoding[:, 0, 1] = self.start[1]
            population_encoding[:, 0, 2] = self.terrain[self.start[0]][
                                                self.start[1]] + self.safe_distance

            for i in range(1, self.encoding_shape[0] - 1):
                point = (int(self.start[0] + i * x), int(self.start[1] + i * y))

                population_encoding[:, i, 0] = point[0] + random_array[:, i, 0]
                population_encoding[:, i, 0] = np.clip(population_encoding[:, i, 0], self.lower[0][0],
                                                       self.upper[0][0]).astype(np.int32)
                population_encoding[:, i, 1] = point[1] + random_array[:, i, 1]
                population_encoding[:, i, 1] = np.clip(population_encoding[:, i, 1], self.lower[0][0],
                                                       self.upper[0][0]).astype(np.int32)
                arr1 = population_encoding[:, i, 0].astype(np.int32)
                arr2 = population_encoding[:, i, 1].astype(np.int32)
                z = self.terrain[arr1, arr2] + self.safe_distance
                population_encoding[:, i, 2] = z

            population_encoding[:, -1, 0] = self.destination[0]
            population_encoding[:, -1, 1] = self.destination[1]
            population_encoding[:, -1, 2] = self.terrain[self.destination[0]][
                                                self.destination[1]] + self.safe_distance
        else:
            population_encoding = population_encoding
        population = self.evaluation(population_encoding)
        self.function_evaluation -= population.len()

        return population

    @staticmethod
    def distance(point1, point2):
        distance = np.linalg.norm(point2 - point1, axis=1)
        return distance

    def _objective_function_length(self, population_encoding):
        fitness = np.zeros([population_encoding.shape[0]])
        for i in range(1, population_encoding.shape[1]):
            fitness += self.distance(population_encoding[:, i - 1, :], population_encoding[:, i, :])
        return fitness

    def _objective_function_threat(self, population_encoding):
        fitness = np.zeros([population_encoding.shape[0]])
        safe = np.ones([population_encoding.shape[0]]) * self.safe_distance
        point = np.zeros([population_encoding.shape[0], 3])
        x_coords = [1, 1, 1, 0, 0, -1, -1, -1]
        y_coords = [-1, 0, 1, -1, 1, -1, 0, 1]
        for i in range(0, population_encoding.shape[1]):
            for (x_coord, y_coord) in zip(x_coords, y_coords):
                x = population_encoding[:, i, 0] + x_coord
                x = np.clip(x, self.lower[0][0], self.upper[0][0]).astype(np.int32)
                point[:, 0] = x
                y = population_encoding[:, i, 1] + y_coord
                y = np.clip(y, self.lower[0][0], self.upper[0][0]).astype(np.int32)
                point[:, 1] = y
                point[:, 2] = self.terrain[x, y]
                fitness += (safe / self.distance(population_encoding[:, i, :], point))
        return fitness

    def calculate_objective(self, population_encoding):
        population_objective = np.zeros([population_encoding.shape[0], self.n_objective])
        population_objective[:, 0] = self._objective_function_length(population_encoding)
        population_objective[:, 1] = self._objective_function_threat(population_encoding)
        return population_objective


# if __name__ == "__main__":
#     p = path_planning_problem()
#     pop = p.initialization()
#     print(pop)
