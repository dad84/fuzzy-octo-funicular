import random
from flask import Flask, render_template
from flask_socketio import SocketIO
from tqdm import tqdm
import eventlet

# Initialize Flask and Flask-SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Define genetic algorithm parameters
pop_size = 5
num_generations = 50
mutation_rate = 0.2
tournament_size = 2

# Define fitness function
def fitness(x):
    return x**2

# Define evolution loop as a separate function
def evolve(socketio):
    # Generate initial population
    pop = [random.uniform(-10, 10) for i in range(pop_size)]

    # Evolution loop
    for i in range(num_generations):
        # Calculate fitness of each individual
        fitness_values = [fitness(x) for x in pop]

        # Select parents for mating (tournament selection)
        parents = []
        while len(parents) < pop_size:
            tournament = random.sample(pop, tournament_size)
            tournament_scalars = [x for x in tournament if not isinstance(x, list)]
            if tournament_scalars:
                winner = max(tournament_scalars, key=fitness)
                parents.append(winner)

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

        # Mutate offspring (random reset mutation)
        for j in range(len(offspring)):
            if random.random() < mutation_rate:
                offspring[j] = random.uniform(-10, 10)

        # Replace population with offspring
        pop = offspring

        # Print best individual in population
        best_ind = max(pop, key=fitness)
        message = "Best individual in generation {}: {:.4f} (fitness = {:.4f})".format(i+1, best_ind, fitness(best_ind))
        socketio.emit('update', message)

        # Sleep for a moment to allow the web page to update
        socketio.sleep(0.1)

# Define Flask routes
@app.route('/')
def index():
    return render_template('index.html')

# Define SocketIO event handlers
@socketio.on('start')
def handle_start():
    # Start the genetic algorithm in a separate thread
    t = socketio.start_background_task(evolve, socketio)

# Start the Flask-SocketIO server
if __name__ == '__main__':
    eventlet.monkey_patch()
    socketio.run(app)
