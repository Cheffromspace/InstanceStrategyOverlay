# import the fetch_strategy function from fetch_strategy.py
from fetch_strategy import fetch_strategy

# specify the path to the input .txt file
input_file = "raids.txt"

# read the contents of the input file
with open(input_file, "r") as file:
    strategies = file.readlines()

# iterate over each strategy in the file
for strategy in strategies:
    # remove any leading/trailing whitespace or newline characters
    strategy = strategy.strip()

    # call the fetch_strategy function for each strategy
    fetch_strategy(strategy, f"./data/fetched_strategies/{strategy}.txt")
