import random

class Puzzle:
    def __init__(self, n):
        self.n = n
        self.size = n * n
        self.initial_config = random.sample(range(self.size), self.size)
        self.target_config = sorted(self.initial_config, reverse=True)

    def fitness(self, config):
        return sum(1 for i in range(self.size) if config[i] == self.target_config[i])

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, self.size - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutation(self, config):
        index1, index2 = random.sample(range(self.size), 2)
        config[index1], config[index2] = config[index2], config[index1]
        return config

    def solve(self, population_size, max_generations):
        population = [self.initial_config] + [self.mutation(self.initial_config) for _ in range(population_size - 1)]
        generation = 0

        while generation < max_generations:
            population = sorted(population, key=self.fitness, reverse=True)
            if population[0] == self.target_config:
                return population[0]

            parents = population[:population_size // 2]
            offspring = [self.crossover(random.choice(parents), random.choice(parents)) for _ in range(population_size - len(parents))]
            population = parents + offspring
            population = [self.mutation(config) for config in population]
            generation += 1

        return None

# Example usage
n = 4  # dimensions of the square matrix
population_size = 100
max_generations = 1000

puzzle = Puzzle(n)
solution = puzzle.solve(population_size, max_generations)

if solution:
    print("Solution found:")
    print(solution)
else:
    print("Solution not found within the given number of generations.")
