import numpy as np
import requests
import time

# Define constants
HISTORICAL_URL = "https://min-api.cryptocompare.com/data/v2/histoday"
CURRENT_URL = "https://min-api.cryptocompare.com/data/price"
FSYM = "BTC"
TSYM = "USD"
LIMIT = 365
NUM_WEIGHTS = 7
POPULATION_SIZE = 5000
NUM_SETS = 5
MUTATION_RATE = 0.001
WAIT_TIME = 30 # seconds
MAX_ITERATIONS = 100
BEST_WEIGHTS_FILE = "best_weights.txt"

def collect_historical_data():
    params = {"fsym": FSYM, "tsym": TSYM, "limit": LIMIT}
    response = requests.get(HISTORICAL_URL, params=params)
    data = response.json()["Data"]["Data"]
    prices = [day["close"] for day in data]
    volumes = [day["volumeto"] for day in data]
    rsis = calculate_rsi(prices)
    return prices, volumes, rsis

def calculate_rsi(prices, window_size=14):
    deltas = np.diff(prices)
    seed = deltas[:1]
    up = deltas[deltas >= 0].sum() / window_size
    down = -deltas[deltas < 0].sum() / window_size
    rs = up / down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsis = [np.nan] * (window_size - 1) + [rsi]
    for i in range(window_size, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0
        else:
            upval = 0
            downval = -delta
        up = (up * (window_size - 1) + upval) / window_size
        down = (down * (window_size - 1) + downval) / window_size
        rs = up / down
        rsi = 100.0 - (100.0 / (1.0 + rs))
        rsis.append(rsi)
    return rsis

def evaluate_weights(weights, prices, rsis):
    weights = np.array(weights) / np.sum(weights)
    prediction = np.dot(prices[-NUM_WEIGHTS:], weights)
    actual = prices[-1]
    rsi = rsis[-1]
    fitness = 1 / abs(prediction - actual) * rsi
    return fitness

def select_top_weights(population, fitness_scores, num_sets):
    top_indices = np.argsort(fitness_scores)[-num_sets:]
    top_weights = population[top_indices, :-1]
    return top_weights

def predict_future_price(prices, top_weights):
    predictions = np.dot(prices[-NUM_WEIGHTS:], top_weights.T)
    response = requests.get(CURRENT_URL, params={"fsym": FSYM, "tsyms": TSYM})
    if response.status_code == 200:
        current_price = response.json().get(TSYM, np.nan)
    else:
        current_price = np.nan
    current_volume = volumes[-1]
    future_price = np.mean(predictions) * (current_price / prices[-1])
    return future_price, current_price, current_volume
    
def generate_new_population(population, fitness_scores):
    new_population = np.zeros((POPULATION_SIZE, NUM_WEIGHTS + 1))
    for i in range(POPULATION_SIZE):
        parent_indices = np.random.choice(POPULATION_SIZE, size=2, replace=False)
        if fitness_scores[parent_indices[0]] > fitness_scores[parent_indices[1]]:
            parent = population[parent_indices[0]]
        else:
            parent = population[parent_indices[1]]
        mutation_mask = np.random.rand(NUM_WEIGHTS) < MUTATION_RATE
        mutation_amounts = np.random.normal(size=NUM_WEIGHTS)
        child = parent[:-1] + mutation_mask * mutation_amounts
        new_population[i, :-1] = child
        new_population[i, -1] = rsis[-1]
    return new_population

# Main program
prices, volumes, rsis = collect_historical_data()

population = np.random.rand(POPULATION_SIZE, NUM_WEIGHTS + 1)
fitness_scores = np.zeros(POPULATION_SIZE)

best_fitness = 0
best_weights = None

for i in range(MAX_ITERATIONS):
    for j in range(POPULATION_SIZE):
        fitness_scores[j] = evaluate_weights(population[j, :-1], prices, rsis)
    top_weights = select_top_weights(population, fitness_scores, NUM_SETS)
    future_price, current_price, current_volume = predict_future_price(prices, top_weights)
    if np.max(fitness_scores) > best_fitness:
        best_fitness = np.max(fitness_scores)
        best_weights = population[np.argmax(fitness_scores), :-1]
        print(f"New best weights found! Fitness score: {best_fitness}")
        np.savetxt(BEST_WEIGHTS_FILE, best_weights)
        print("Best weights saved to file.")
    new_population = generate_new_population(population, fitness_scores)
    population = new_population
    rsis = rsis[1:] + [rsis[-1]]
    prices = prices[1:] + [future_price]
    volumes = volumes[1:] + [current_volume]
    print(f"Iteration {i+1}: current price={current_price:.2f}, predicted future price={future_price:.2f}")
    time.sleep(WAIT_TIME)
    
