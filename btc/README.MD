# Real-time Trading Strategy Optimization

This Python program uses a real-time trading strategy optimization algorithm to identify the best weights for a given set of market data.

## Prerequisites

This program requires the following packages to be installed:

- `numpy`
- `websocket-client`

## How to Run

1. Clone this repository to your local machine.
2. Install the required packages listed above.
3. Run the script using `BTCga.py`.
4. The script will begin to stream market data from the Binance WebSocket API and optimize the trading strategy in real-time.

## Overview

This program uses the Binance WebSocket API to stream real-time market data for BTCUSDT. It calculates the Relative Strength Index (RSI) for the past 14 days and uses a genetic algorithm to optimize a trading strategy that predicts future prices.

The program generates a population of 500 sets of weights, with 7 weights in each set. It then evaluates the fitness of each set of weights by calculating a score based on how closely the predicted price matches the actual price and the RSI value at the time of prediction. The program then selects the top 5 sets of weights with the highest fitness scores and uses them to make predictions for the future price.

The program saves the best set of weights found so far to a file called `best_weights.txt`. The program also prints out the current market data, including the current price, current volume, and predicted future price.

The program continues to run indefinitely, optimizing the trading strategy in real-time as new market data becomes available. It will stop after 100 iterations.

## Sample Output

Here is an example of what the program output might look like:

```
New best weights found! Fitness score: 188.03534070514598
Best weights saved to file.
Iteration 10: current price=23562.96, predicted future price=23629.68
```

## How it Works

The program uses a WebSocket connection to stream real-time market data from the Binance API. It calculates the RSI for the past 14 days based on the price data received from the API. It then generates a population of 500 sets of weights, each with 7 weights.

The program evaluates the fitness of each set of weights by calculating a score based on how closely the predicted price matches the actual price and the RSI value at the time of prediction. The program then selects the top 5 sets of weights with the highest fitness scores and uses them to make predictions for the future price.

The program saves the best set of weights found so far to a file called `best_weights.txt`. The program also prints out the current market data, including the current price, current volume, and predicted future price.

The program continues to run indefinitely, optimizing the trading strategy in real-time as new market data becomes available. It will stop after 100 iterations.

## v0.3 Some of the changes I made to the code include:

1. Defining constants at the top of the script to make it easier to modify them later on.
2. Separating the data collection and processing functions into separate functions for readability and maintainability.
3. Modifying the calculate_rsi function to handle the first 14 days separately and to calculate the RSI for all subsequent days.
4. Adding a check to the predict_future_price function to handle cases where the API response does not contain the expected currency data.
5. Adding a call to np.savetxt to save the best weights to a file when they are updated.
6. Adding calls to rsis.append(rsi) and prices.append(future_price) to update the lists of prices and RSI values at the end of each iteration.
7. Adding a loop over the iterations and a call to time.sleep to wait between API requests.
8. Fixing the incomplete generate_new_population function to generate new child sets of weights with mutations applied to one of the parents.

## Credits

This program was written by dad84 and is licensed under the [MIT License](https://opensource.org/licenses/MIT).
