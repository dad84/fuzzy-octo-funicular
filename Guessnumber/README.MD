# Genetic Algorithm

This is a simple implementation of a Genetic Algorithm (GA) in Python. The GA is a heuristic optimization algorithm that is inspired by the process of natural selection. It can be used to solve many optimization problems, including those in which the objective function is complex, non-linear, and noisy.

## Usage

To use this GA, simply run the code in a Python environment. The script contains several parameters that you can modify to adjust the behavior of the algorithm:

- `POPULATION_SIZE`: The size of the population. This determines how many individuals are in each generation of the GA.
- `MIN_NUMBER` and `MAX_NUMBER`: The range of the possible numbers. This determines the range of the random numbers used to create the initial population and to generate the target number for each generation.
- `NUM_GENERATIONS`: The number of generations to run the algorithm. This determines how long the GA will run before stopping.
- `mutation_rate`: The mutation rate, which determines the probability that an individual will be randomly mutated in each generation.

## Implementation

This GA is implemented using the following functions:

- `fitness(guess, number)`: The fitness function, which calculates the fitness of an individual by measuring how close its guess is to the target number.
- `create_individual()`: The create_individual function, which generates a random guess within the given range of possible numbers.
- `crossover(parent1, parent2)`: The crossover function, which combines two parents' guesses by taking their average.
- `mutate(individual)`: The mutate function, which randomly adjusts an individual's guess within a small range.

The GA works by creating an initial population of random individuals, and then running a loop for a fixed number of generations. In each generation, the GA calculates the fitness of each individual, selects the best individuals to become parents for the next generation, and creates a new population by combining and mutating the parents' guesses.

## Examples

Here's an example of how to run the GA with the default parameters:

```python
import random

# Define the size of the population
POPULATION_SIZE = 100

# Define the range of the possible numbers
MIN_NUMBER = 1
MAX_NUMBER = 100

# Define the number of generations to run the algorithm
NUM_GENERATIONS = 100

# Define the mutation rate
mutation_rate = 0.1

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
    # Print the best individual
    print("Generation {}: Best Guess = {}, Best Fitness = {}".format(generation, best_guess, best_fitness))
    # Select the parents for the next generation
    weights = [1.0 / (fit + 0.0001) for fit in fitnesses] # add a small constant to prevent division by zero
    parents = random.choices(population, weights=weights, k=2)
    # Create the next generation
    next_generation = [crossover(parents[0], parents[1]) for i in range(POPULATION_SIZE)]
    # Mutate some of the individuals in the next generation
    for i in range(POPULATION_SIZE):
        if random.random() < mutation_rate:
            next_generation[i] = mutate(next_generation[i])
    # Update the population for the next generation
    population = next_generation
    
