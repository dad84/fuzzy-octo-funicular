import numpy as np
import requests
import time

historical_url = "https://min-api.cryptocompare.com/data/v2/histoday"
params = {
    "fsym": "BTC",
    "tsym": "USD",
    "limit": 365
}
response = requests.get(historical_url, params=params)
data = response.json()["Data"]["Data"]

prices = []
volumes = []
rsi = []
for day in data:
    timestamp = day["time"]
    price = day["close"]
    volume = day["volumeto"]
    prices.append(price)
    volumes.append(volume)

    if len(prices) > 14:
        # Calculate RSI for the past 14 days
        deltas = np.diff(prices[-14:])
        seed = deltas[:1]
        up = deltas[deltas >= 0].sum() / 14
        down = -deltas[deltas < 0].sum() / 14
        rs = up / down
        rsi.append(100.0 - (100.0 / (1.0 + rs)))
    else:
        rsi.append(np.nan)

print("Historical data collected")


def fitness_function(weights, rsi):
    weights = np.array(weights) / np.sum(weights)
    prediction = np.dot(prices[-7:], weights)
    actual = prices[-1]
    rsi_value = rsi[-1]
    fitness = 1 / abs(prediction - actual) * rsi_value
    return fitness

population_size = 500
num_weights = 7
mutation_rate = 0.01
num_sets = 5

population = np.random.rand(population_size, num_weights + 1)
fitness_scores = np.zeros(population_size)

best_fitness = 0
best_weights = None

counter = 0

while True:
    for i in range(population_size):
        fitness_scores[i] = fitness_function(population[i, :-1], rsi)
    top_indices = np.argsort(fitness_scores)[-num_sets:]
    top_weights = population[top_indices, :-1]
    predictions = np.zeros(num_sets)
    for i in range(num_sets):
        predictions[i] = np.dot(prices[-7:], top_weights[i])
    current_url = "https://min-api.cryptocompare.com/data/price"
    params = {
        "fsym": "BTC",
        "tsyms": "USD"
    }
    response = requests.get(current_url, params=params)
    if response.status_code == 200:
        current_data = response.json()
        if "USD" in current_data:
            current_price = current_data["USD"]
            current_volume = volumes[-1]
            future_price = np.mean(predictions) * (current_price / prices[-1])
            if np.max(fitness_scores) > best_fitness:
                best_fitness = np.max(fitness_scores)
                best_weights = population[np.argmax(fitness_scores), :-1]
                print("New best weights found! Fitness score:", best_fitness)
        else:
            raise ValueError("Error: no USD data found in API response.")
    else:
        print("Error: API request failed.")
        continue
    counter += 1
    if counter > 100:
        break
    time.sleep(30)
    current_volume = volumes[-1]
    future_price = np.mean(predictions) * (current_price / prices[-1])
    if np.max(fitness_scores) > best_fitness:
        best_fitness = np.max(fitness_scores)
        best_weights = population[np.argmax(fitness_scores), :-1]
    new_population = np.zeros((population_size, num_weights + 1))
    for i in range(population_size):
        parent_indices = np.random.choice(population_size, size=2, replace=False)
        if fitness_scores[parent_indices[0]] > fitness_scores[parent_indices[1]]:
            parent = population[parent_indices[0]]
        else:
            parent = population[parent_indices[1]]
        mutation_mask = np.random.rand(num_weights) < mutation_rate
        mutation_amounts = np.random.normal(size=num_weights)
        child = parent[:-1] + mutation_mask * mutation_amounts
        new_population[i, :-1] = child
        new_population[i, -1] = rsi[-1]
    population = new_population
    
    print("Current market data collected")
    print("Current price:", current_price)
    print("Current volume:", current_volume)
    print("Predicted future price:", future_price)
    
if np.max(fitness_scores) > best_fitness:
    best_fitness = np.max(fitness_scores)
    best_weights = population[np.argmax(fitness_scores), :-1]
    print("New best weights found! Fitness score:", best_fitness)
save_result = np.savetxt("best_weights.txt", best_weights)
if save_result is None:
    print("Best weights saved to file.")
else:
    print("Error saving best weights to file:", save_result)
