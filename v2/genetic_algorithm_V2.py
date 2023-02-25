import multiprocessing
import random
from tqdm import tqdm
from multiprocessing import Pool

# Fitness function (to be optimized)
def fitness(x):
    return x**2

# Genetic algorithm parameters
pop_size = 50
num_generations = 100
mutation_rate = 0.2
elitism = 2
num_cpus = 4

# Initialization parameters
initialization = 'sobol'

# Selection parameters
selection = 'tournament'
tournament_size = 5

# Crossover parameters
crossover = 'uniform'
crossover_prob = 0.8

# Mutation parameters
mutation = 'gaussian'
mutation_scale = 0.1
adaptive_mutation = True
adaptive_mutation_step = 0.01
adaptive_mutation_threshold = 0.2

# Initialize population
def initialize_population(size, initialization):
    if initialization == 'random':
        return [random.uniform(-10, 10) for i in range(size)]
    elif initialization == 'latin_hypercube':
        pass # TODO: Implement Latin hypercube sampling
    elif initialization == 'sobol':
        pass # TODO: Implement Sobol sequences

pop = initialize_population(pop_size, initialization)

# Evaluate fitness of population
def evaluate_population(population):
    with multiprocessing.Pool() as p:
        fitness_values = p.map(fitness, population)
    return fitness_values

# Evolution loop
print("Starting evolution...")
for i in tqdm(range(num_generations)):
    # Evaluate fitness of population
    fitness_values = evaluate_population(pop)

    # Select elites from population
    elites = sorted(zip(pop, fitness_values), key=lambda x: x[1], reverse=True)[:elitism]

    # Select parents for mating
    parents = selection(pop, fitness_values, num_parents)

    # Create offspring via crossover and mutation
    offspring = crossover(parents, pop_size - elitism)
    offspring = mutation(offspring, mutation_rate, mutation_scale)

    # Evaluate fitness of offspring
    offspring_fitness = evaluate_population(offspring)

    # Merge parents and offspring
    pop = elites + offspring
    fitness_values = [elite[1] for elite in elites] + offspring_fitness

    # Print best individual in population
    best_ind = max(pop, key=fitness)
    tqdm.write("Best individual in generation {}: {:.4f} (fitness = {:.4f})".format(i+1, best_ind, fitness(best_ind)))

    
    # Crossover
    for j in range(0, len(parents)-1, 2):
        if random.random() < crossover_prob:
            if crossover == 'single_point':
                crossover_point = random.randint(1, len(parents[j])-1)
                offspring += [parents[j][:crossover_point] + parents[j+1][crossover_point:],
                              parents[j+1][:crossover_point] + parents[j][crossover_point:]]
            elif crossover == 'uniform':
                child1 = []
                child2 = []
                for k in range(len(parents[j])):
                    if random.random() < 0.5:
                        child1.append(parents[j][k])
                        child2.append(parents[j+1][k])
                    else:
                        child1.append(parents[j+1][k])
                        child2.append(parents[j][k])
                offspring += [child1, child2]
    
    # Mutation
if adaptive_mutation:
    avg_fitness = sum(fitness_values) / pop_size
    stddev_fitness = (sum((f-avg_fitness)**2 for f in fitness_values) / pop_size)**0.5
    if stddev_fitness > adaptive_mutation_threshold * avg_fitness:
        mutation_rate = max(0, mutation_rate - adaptive_mutation_step)
    else:
        mutation_rate = min(1, mutation_rate + adaptive_mutation_step)
    
    for j in range(len(offspring)):
        if random.random() < mutation_rate:
            if mutation == 'random_reset':
                offspring[j] = random.uniform(-10, 10)
            elif mutation == 'gaussian':
                offspring[j] += random.gauss(0, mutation_scale)
                offspring[j] = max(-10, min(10, offspring[j]))

    # Evaluate fitness of offspring
    offspring_fitness = evaluate_population(offspring)
    
    # Merge parents and offspring
    pop = elites + offspring
    fitness_values = [elite[1] for elite in elites] + offspring_fitness
    
    # Print best individual in population
    best_ind = max(pop, key=fitness)
    tqdm.write("Best individual in generation {}: {:.4f} (fitness = {:.4f})".format(i+1, best_ind, fitness(best_ind)))
