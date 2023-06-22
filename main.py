import random

def generate_initial_state(n):
    numbers = list(range(1, n**2))
    numbers.append(0)
    random.shuffle(numbers)
    initial_state = [numbers[i:i+n] for i in range(0, len(numbers), n)]
    return initial_state

def calculate_fitness(chromosome, goal_state):
    fitness = sum([1 for i in range(len(chromosome)) if chromosome[i] != goal_state[i]])
    return fitness

def proportional_selection(population, fitness_values):
    fitness_sum = sum(fitness_values)
    probabilities = [fitness / fitness_sum for fitness in fitness_values]

    selected_parents = random.choices(population, probabilities, k=len(population) // 2)
    
    return selected_parents

def crossover(parent1, parent2):
    n = len(parent1)
    crossover_point = random.randint(1, n*n - 1)
    child1 = parent1.copy()
    child2 = parent2.copy()

    flattened_parent1 = [gene for row in parent1 for gene in row]
    flattened_parent2 = [gene for row in parent2 for gene in row]

    child1_genes = flattened_parent1[:crossover_point] + flattened_parent2[crossover_point:]
    child2_genes = flattened_parent2[:crossover_point] + flattened_parent1[crossover_point:]

    child1 = [child1_genes[i:i+n] for i in range(0, n*n, n)]
    child2 = [child2_genes[i:i+n] for i in range(0, n*n, n)]

    return child1, child2

def mutation(chromosome, mutation_rate):
    mutated_chromosome = []
    for row in chromosome:
        mutated_row = row[:]
        for i in range(len(row)):
            if random.random() < mutation_rate:
                mutation_value = random.randint(0, len(row) - 1)
                while mutation_value == row[i]:
                    mutation_value = random.randint(0, len(row) - 1)
                mutated_row[i] = mutation_value
        mutated_chromosome.append(mutated_row)
    return mutated_chromosome

def genetic_algorithm(n, population_size, mutation_rate, max_generations):
    goal_state = list(range(1, n**2))
    goal_state.append(0)
    population = [generate_initial_state(n) for _ in range(population_size)]

    for generation in range(max_generations):
        fitness_values = [calculate_fitness(chromosome, goal_state) for chromosome in population]
        selected_parents = proportional_selection(population, fitness_values)

        new_population = []
        while len(new_population) < population_size:
            parent1 = random.choice(selected_parents)
            parent2 = random.choice(selected_parents)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population[:population_size]

    best_chromosome = min(population, key=lambda chromosome: calculate_fitness(chromosome, goal_state))
    return best_chromosome

# Example usage
n = 3  # Size of the puzzle (3x3 in this case)
population_size = 20  # Number of individuals in the population
mutation_rate = 0.1  # Probability of mutation for each gene
max_generations = 100  # Maximum number of generations

solution = genetic_algorithm(n, population_size, mutation_rate, max_generations)

# Print the solution
for row in solution:
    print(row)
