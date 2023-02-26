import random
import pygame

# Define the state space of the Snake game
state_space = 4

# Define the size of the population
population_size = 50

# Define the number of generations to run the algorithm
num_generations = 100

# Define the size of the game board
board_width = 20
board_height = 20

# Initialize the pygame library
pygame.init()

# Set the size of the game window
window_size = (500, 500)
screen = pygame.display.set_mode(window_size)

# Set up the game window
pygame.display.set_caption("Snake Game")

# Define the colors used in the game
background_color = (255, 255, 255)
snake_color = (0, 0, 255)
food_color = (255, 0, 0)

def fitness_function(genotype):
    # Define the initial position and velocity of the Snake
    snake_x = board_width // 2
    snake_y = board_height // 2
    snake_dx, snake_dy = 0, -1
    
    # Define the initial position of the food
    food_x, food_y = random.randint(0, board_width-1), random.randint(0, board_height-1)
    
    # Define the initial state of the game
    score = 0
    snake_length = 1
    snake_list = [(snake_x, snake_y)]
    game_over = False
    
    # Run the game loop
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        
        # Update the position of the Snake based on its velocity
        snake_x += snake_dx
        snake_y += snake_dy
        
        # Check if the Snake has collided with the walls or its own body
        if snake_x < 0 or snake_x >= board_width or snake_y < 0 or snake_y >= board_height:
            game_over = True
        for segment in snake_list[:-1]:
            if segment == (snake_x, snake_y):
                game_over = True
        
        # Check if the Snake has eaten the food
        if snake_x == food_x and snake_y == food_y:
            score += 1
            snake_length += 1
            food_x, food_y = random.randint(0, board_width-1), random.randint(0, board_height-1)
        
        # Update the position of the Snake's body
        snake_list.append((snake_x, snake_y))
        if len(snake_list) > snake_length:
            del snake_list[0]
        
        # Update the velocity of the Snake based on the genotype
        input_vector = [snake_x-food_x, snake_y-food_y, snake_dx, snake_dy]
        output_vector = [sum([input_vector[i]*genotype[i] for i in range(len(genotype))])]
        snake_dx += int(output_vector[0])
        snake_dy += int(output_vector[0])
        
        # Draw the game board
        screen.fill(background_color)
        for segment in snake_list:
            pygame.draw.rect(screen, snake_color, (segment[0]*20, segment[1]*20, 20, 20))
        pygame.draw.rect(screen, food_color, (food_x*20, food_y*20, 20, 20))
        pygame.display.update()
        
        # Check if the game is over
        if game_over:
            break
            
        # Return the fitness score based on the final score of the game
    return score


def selection_function(population):
    # Define the tournament size
    tournament_size = 5
    
    # Randomly select a set of individuals from the population
    tournament_indices = random.sample(range(len(population)), tournament_size)
    tournament_scores = [fitness_function(population[i]) for i in tournament_indices]
    
    # Return the index of the fittest individual in the tournament
    return tournament_indices[tournament_scores.index(max(tournament_scores))]


def crossover_function(parent1, parent2):
    # Define the probability of crossover
    crossover_prob = 0.5
    
    # Perform single-point crossover between the parents with a probability of crossover_prob
    if random.random() < crossover_prob:
        crossover_point = random.randint(1, len(parent1)-1)
        offspring = parent1[:crossover_point] + parent2[crossover_point:]
    else:
        offspring = parent1
    
    # Return the offspring genotype
    return offspring


def mutation_function(genotype):
    # Define the probability of mutation
    mutation_prob = 0.1
    
    # Perform random uniform mutation on the genotype with a probability of mutation_prob
    mutated_genotype = []
    for gene in genotype:
        if random.random() < mutation_prob:
            mutated_gene = gene + random.uniform(-0.1, 0.1)
        else:
            mutated_gene = gene
        mutated_genotype.append(mutated_gene)
    
    # Return the mutated genotype
    return mutated_genotype


# Generate the initial population
population = []
for i in range(population_size):
    genotype = [random.uniform(-1, 1) for i in range(state_space)]
    population.append(genotype)

# Run the genetic algorithm
for i in range(num_generations):
    # Evaluate the fitness of each individual in the population
    fitness_scores = [fitness_function(genotype) for genotype in population]
    
    # Select parents for reproduction
    parents = []
    for j in range(population_size // 2):
        parent1_index = selection_function(population)
        parent2_index = selection_function(population)
        parents.append((parent1_index, parent2_index))
    
    # Reproduce and mutate the genotypes
    offspring = []
    for parent1_index, parent2_index in parents:
        parent1 = population[parent1_index]
        parent2 = population[parent2_index]
        offspring_genotype = crossover_function(parent1, parent2)
        mutated_genotype = mutation_function(offspring_genotype)
        offspring.append(mutated_genotype)
    
    # Replace the old population with the new offspring
    population = offspring

    # Print the best fitness score for each generation
    best_fitness = max(fitness_scores)
    print("Generation:", i+1, "Best fitness:", best_fitness)

# Run the game with the best individual from the final generation
best_individual = max(population, key=fitness_function)
fitness = fitness_function(best_individual)

print("Best individual:", best_individual)
print("Fitness:", fitness)

# Define the initial position and velocity of the Snake
snake_x = board_width // 2
snake_y = board_height // 2
snake_dx, snake_dy = 0, -1

# Define the initial position of the food
food_x, food_y = random.randint(0, board_width-1), random.randint(0, board_height-1)

# Define the initial state of the game
score = 0
snake_length = 1
snake_list = [(snake_x, snake_y)]
game_over = False

# Run the game
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    
    # Update the position of the Snake based on its velocity
    snake_x += snake_dx
    snake_y += snake_dy
    
    # Check if the Snake has collided with the walls or its own body
    if snake_x < 0 or snake_x >= board_width or snake_y < 0 or snake_y >= board_height:
        # Snake has crashed into the wall
        print("Snake has crashed into the wall!")
        game_over = True
    for segment in snake_list[:-1]:
        if segment == (snake_x, snake_y):
            # Snake has crashed into itself
            print("Snake has crashed into itself!")
            game_over = True
    
    # Check if the Snake has eaten the food
    if snake_x == food_x and snake_y == food_y:
        print("Snake has eaten the food!", flush=True)
        score += 1
        snake_length += 1
        food_x, food_y = random.randint(0, board_width-1), random.randint(0, board_height-1)
    
    # Update the position of the Snake's body
    snake_list.append((snake_x, snake_y))
    if len(snake_list) > snake_length:
        del snake_list[0]
    
    # Update the velocity of the Snake based on the genotype
    input_vector = [snake_x-food_x, snake_y-food_y, snake_dx, snake_dy]
    output_vector = [sum([input_vector[i]*best_individual[i] for i in range(len(best_individual))])]
    snake_dx += int(output_vector[0])
    snake_dy += int(output_vector[0])
    
    # Draw the game board
    screen.fill(background_color)
    for segment in snake_list:
        pygame.draw.rect(screen, snake_color, (segment[0]*20, segment[1]*20, 20, 20))
    pygame.draw.rect(screen, food_color, (food_x*20, food_y*20, 20, 20))
    pygame.display.update()
   
    # Delay for 500 milliseconds
    pygame.time.delay(500)
   
    # Check if the game is over
    if game_over:
        break

# Print the final score and genotype of the best individual
print("Final score:", score)
print("Best individual:", best_individual)
print("Fitness:", fitness)

# Quit the game
pygame.quit()

    
