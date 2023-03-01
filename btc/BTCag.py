import numpy as np
import requests
import time

# Gather historical data from CryptoCompare API
historical_url = "https://min-api.cryptocompare.com/data/v2/histoday"
params = {
    "fsym": "BTC",
    "tsym": "USD",
    "limit": 365
}
response = requests.get(historical_url, params=params)
data = response.json()["Data"]["Data"]

# Extract price and volume data from historical data
prices = []
volumes = []
for day in data:
    timestamp = day["time"]
    price = day["close"]
    volume = day["volumeto"]
    prices.append(price)
    volumes.append(volume)

# Define the problem
def fitness_function(weights):
    # Normalize the weights
    weights = np.array(weights) / np.sum(weights)
    # Use the weights to predict the next day's price
    prediction = np.dot(prices[-7:], weights)
    actual = prices[-1]
    # Calculate the fitness as the inverse of the absolute error
    fitness = 1 / abs(prediction - actual)
    return fitness

# Create the GA program
population_size = 50
num_weights = 7
mutation_rate = 0.1
num_sets = 5 # Number of sets of weights to use for ensemble

population = np.random.rand(population_size, num_weights)
fitness_scores = np.zeros(population_size)

best_fitness = 0
best_weights = None

while True:
    # Evaluate fitness for each individual in the population
    for i in range(population_size):
        fitness_scores[i] = fitness_function(population[i])
    # Find the top n individuals in the population
    top_indices = np.argsort(fitness_scores)[-num_sets:]
    top_weights = population[top_indices]
    # Use ensemble methods to predict future prices
    predictions = np.zeros(num_sets)
    for i in range(num_sets):
        predictions[i] = np.dot(prices[-7:], top_weights[i])
    # Gather current market data from CryptoCompare API
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
        else:
            print("Error: no USD data found in API response.")
            continue
    else:
        print("Error: API request failed.")
        continue
    current_volume = volumes[-1]  # We can use the last known volume
    future_price = np.mean(predictions) * (current_price / prices[-1])
    # Update best fitness and weights
    if np.max(fitness_scores) > best_fitness:
        best_fitness = np.max(fitness_scores)
        best_weights = population[np.argmax(fitness_scores)]
    # Create a new population through selection and mutation
    new_population = np.zeros((population_size, num_weights))
    for i in range(population_size):
        # Tournament selection
        parent_indices = np.random.choice(population_size, size=2, replace=False)
        if fitness_scores[parent_indices[0]] > fitness_scores[parent_indices[1]]:
            parent = population[parent_indices[0]]
        else:
            parent = population[parent_indices[1]]
        # Mutation
        mutation_mask = np.random.rand(num_weights) < mutation_rate
        mutation_amounts = np.random.normal(size=num_weights)
        child = parent + mutation_mask * mutation_amounts
        new_population[i] = child
    population = new_population
    
    # Wait for 30 seconds before updating current market data
    time.sleep(30)
    
    print("Current price:", current_price)
    print("Current volume:", current_volume)
    print("Predicted future price:", future_price)
