import random

# Define the size of the population
POPULATION_SIZE = 100

# Define the range of the possible numbers
MIN_NUMBER = 1
MAX_NUMBER = 100

# Define the number of generations to run the algorithm
NUM_GENERATIONS = 100

# Define the fitness function
def fitness(guess, number):
    return abs(guess - number)

# Define the create_individual function to create a random guess
def create_individual():
    return random.randint(MIN_NUMBER, MAX_NUMBER)

# Define the crossover function to combine two guesses
def crossover(parent1, parent2):
    child = (parent1 + parent2) // 2
    return child

# Define the mutate function to randomly adjust a guess
def mutate(individual):
    mutation_amount = random.randint(-10, 10)
    individual += mutation_amount
    individual = max(individual, MIN_NUMBER)
    individual = min(individual, MAX_NUMBER)
    return individual

# Create the initial population
population = [create_individual() for i in range(POPULATION_SIZE)]

# Run the algorithm for a fixed number of generations
for generation in range(NUM_GENERATIONS):
    # Generate a random number for the game
    number = random.randint(MIN_NUMBER, MAX_NUMBER)
    # Calculate the fitness of each individual in the population
    fitnesses = [fitness(guess, number) for guess in population]
    # Find the best individual in the population
    best_fitness = min(fitnesses)
    best_guess = population[fitnesses.index(best_fitness)]
    # Print the best individual for each generation
    print("Generation {}: Best Guess = {}, Best Fitness = {}".format(generation, best_guess, best_fitness))
    # Select the parents for the next generation
    weights = [1.0 / (fit + 0.0001) for fit in fitnesses] # add a small constant to prevent division by zero
    parents = random.choices(population, weights=weights, k=2)
    # Create the next generation
    next_generation = [crossover(parents[0], parents[1]) for i in range(POPULATION_SIZE)]
    # Mutate some of the individuals in the next generation
    for i in range(POPULATION_SIZE):
        if random.random() < 0.1:
            next_generation[i] = mutate(next_generation[i])
    # Update the population for the next generation
    population = next_generation
