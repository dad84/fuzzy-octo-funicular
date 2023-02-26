import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 500
window_height = 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Set up the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Set up the font
font = pygame.font.SysFont(None, 25)

# Set up the clock
clock = pygame.time.Clock()

# Set up the snake starting position and speed
snake_size = 10
snake_speed = 15
snake_x = window_width / 2
snake_y = window_height / 2
snake_x_change = 0
snake_y_change = 0

# Set up the food starting position
food_size = 10
food_x = round(random.randrange(0, window_width - food_size) / 10.0) * 10.0
food_y = round(random.randrange(0, window_height - food_size) / 10.0) * 10.0

# Set up the score
score = 0

# Define a function to display the score
def display_score(score):
    score_text = font.render("Score: " + str(score), True, white)
    window.blit(score_text, [0, 0])

# Define a function to draw the snake
def draw_snake(snake_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, black, [x[0], x[1], snake_size, snake_size])

# Define the game loop
def game_loop():
    # Make the snake global so we can modify it
    global snake_x, snake_y, snake_x_change, snake_y_change, score, food_x, food_y
    
    # Set up the snake starting length and list
    snake_length = 1
    snake_list = []
    
    # Set up the game over flag
    game_over = False
    
    # Initialize the food position
    food_x = round(random.randrange(0, window_width - food_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, window_height - food_size) / 10.0) * 10.0
    
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -snake_size
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = snake_size
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_y_change = -snake_size
                    snake_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_y_change = snake_size
                    snake_x_change = 0
        
        # Move the snake
        snake_x += snake_x_change
        snake_y += snake_y_change
        
        # Check for collision with the walls
        if snake_x < 0 or snake_x >= window_width or snake_y < 0 or snake_y >= window_height:
            game_over = True
        
        # Check for collision with the food
        if snake_x == food_x and snake_y == food_y:
            food_x = round(random.randrange(0, window_width - food_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, window_height - food_size) / 10.0) * 10.0
            snake_length += 1
            score += 10
        
             # Draw the game objects
        window.fill(red)
        pygame.draw.rect(window, white, [food_x, food_y, food_size, food_size])
        
        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)
        
        if len(snake_list) > snake_length:
            del snake_list[0]
        
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True
        
        draw_snake(snake_size, snake_list)
        
        display_score(score)
        
        pygame.display.update()
        
        # Set the frame rate
        clock.tick(snake_speed)
    
    # Quit Pygame and exit the program
    pygame.quit()
    quit()

# Start the game loop
game_loop()

