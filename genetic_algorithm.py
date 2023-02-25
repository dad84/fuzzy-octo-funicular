import random
from tqdm import tqdm

# Fitness function (to be optimized)
def fitness(x):
    return x**2

# Genetic algorithm parameters
pop_size = 5
num_generations = 50
mutation_rate = 0.2

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

    # Select parents for mating (roulette wheel selection)
    total_fitness = sum(fitness_values)
    parent_probs = [f/total_fitness for f in fitness_values]
    parents = [pop[i] for i in range(pop_size) if random.random() < parent_probs[i] and type(pop[i]) == list]
    
    # Create offspring via crossover (single-point crossover)
    offspring = []
    while len(offspring) < pop_size - len(parents):
        if len(parents) >= 2:
            parent1, parent2 = random.sample(parents, 2)
            crossover_point = random.randint(1, len(parent1)-1)
            offspring.append(parent1[:crossover_point] + parent2[crossover_point:])
    
    # Add parents to offspring
    offspring += parents
    
    # Mutate offspring (random reset mutation)
    for j in range(len(offspring)):
        if random.random() < mutation_rate:
            if type(offspring[j]) == list:
                offspring[j] = [random.uniform(-10, 10)]
            else:
                offspring[j] = random.uniform(-10, 10)
    
    # Replace population with offspring
    pop = offspring
    
    # Print best individual in population
    best_ind = max(pop, key=fitness)
    tqdm.write("Best individual in generation {}: {:.4f} (fitness = {:.4f})".format(i+1, best_ind, fitness(best_ind)))
