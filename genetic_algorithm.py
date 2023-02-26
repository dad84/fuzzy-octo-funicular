import random
from tqdm import tqdm

# Fitness function (to be optimized)
def fitness(x):
    return x**2

# Genetic algorithm parameters
pop_size = 5
num_generations = 50
mutation_rate = 0.2
tournament_size = 2

# Generate initial population
pop = [random.uniform(-10, 10) for i in range(pop_size)]

# Print initial population
print("Initial population:")
for ind in pop:
    print(ind)

# Evolution loop
print("Starting evolution...")
for i in tqdm(range(num_generations)):
    # Calculate fitness of each individual
    fitness_values = [fitness(x) for x in pop]
    print("Fitness values:", fitness_values)

    # Select parents for mating (tournament selection)
    parents = []
    while len(parents) < pop_size:
        tournament = random.sample(pop, tournament_size)
        tournament_scalars = [x for x in tournament if not isinstance(x, list)]
        if tournament_scalars:
            winner = max(tournament_scalars, key=fitness)
            parents.append(winner)
    print("Parents:", parents)

    # Create offspring via crossover (variable-length crossover)
    offspring = []
    while len(offspring) < pop_size:
        parent1, parent2 = random.sample(parents, 2)
        if isinstance(parent1, list) and isinstance(parent2, list):
            crossover_point = random.randint(1, min(len(parent1), len(parent2))-1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            offspring.append(child[0])
        elif not isinstance(parent1, list) and not isinstance(parent2, list):
            crossover_point = random.randint(1, 2)
            if crossover_point == 1:
                child = [parent1, parent2]
            else:
                child = [parent2, parent1]
            offspring.append(child[0])
    print("Offspring after crossover:", offspring)

    # Mutate offspring (random reset mutation)
    for j in range(len(offspring)):
        if random.random() < mutation_rate:
            offspring[j] = random.uniform(-10, 10)
    print("Offspring after mutation:", offspring)

    # Replace population with offspring
    pop = offspring

    # Print best individual in population
    best_ind = max(pop, key=fitness)
    tqdm.write("Best individual in generation {}: {:.4f} (fitness = {:.4f})".format(i+1, best_ind, fitness(best_ind)))
