# Genetic Algorithm for Bitcoin Price Prediction

This Python script uses a genetic algorithm to predict the future price of Bitcoin based on historical price data and relative strength index (RSI) values. 

## Usage

1. Install the required Python libraries.

2. Run the script using `python3 btc.py`.

3. Wait for the script to finish running. The script will make API requests to CryptoCompare to collect historical price and volume data for Bitcoin, and then use a genetic algorithm to optimize a set of weights that can predict the future price of Bitcoin based on the past 7 days of price data and RSI values.

4. The script will output the current market data, including the current price and volume of Bitcoin, as well as the predicted future price based on the optimized weights.

5. Once the script has finished running, it will save the best weights to a text file called `best_weights.txt`.

## How It Works

1. The script first retrieves 365 days of daily price and volume data for Bitcoin from the CryptoCompare API using the requests library.

2. It then calculates the RSI for each day using the previous 14 days of closing prices.

3. The fitness function takes in a set of weights (7 in total) and the RSI values, and returns a fitness score based on how well the weighted average of the last 7 days of prices predicts the next day's price, multiplied by the RSI value for the current day.

4. The genetic algorithm then iterates over a fixed number of generations, with each generation consisting of creating a new population of weights based on the previous generation's fitness scores and randomly selecting parents from the population to create children with slight mutations. 

5. The top-performing weights from each generation are then used to make predictions for the future price of Bitcoin, and if the current fitness score is higher than the previous best score, the weights are updated as the new best weights.

6. Finally, the script saves the best weights to a text file.
