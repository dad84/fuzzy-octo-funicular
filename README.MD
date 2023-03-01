# Bitcoin Price Prediction Using Genetic Algorithm

This is a Python script that uses a genetic algorithm (GA) to predict the future price of Bitcoin (BTC) based on historical price and volume data. The script uses the CryptoCompare API to gather historical and current market data, and defines a fitness function that calculates the fitness of a set of weights used to predict the future price.

## Installation

Before running the script, you need to install the required libraries. You can do this using `pip`:

`pip install numpy requests`


## Usage

To use the script, simply run it using Python:

`btcag.py`


The script will start running and will output the current market data and predicted future price every 30 seconds. It will also update the best fitness and weights based on the fitness of the current population.

## Parameters

The script defines several parameters for the GA program, which you can adjust to customize the program:

- `population_size`: The size of the population of sets of weights.
- `num_weights`: The number of weights to use to predict the future price.
- `mutation_rate`: The probability of mutation for each weight.
- `num_sets`: The number of sets of weights to use for ensemble methods.

You can adjust these parameters to see how they affect the predictions made by the script.

## Disclaimer

Financial markets are highly complex and unpredictable, and past performance does not guarantee future results. Therefore, any predictions made by this script should be taken with a grain of salt and should not be relied upon for investment decisions.

## License

This script is released under the [MIT License](LICENSE).
