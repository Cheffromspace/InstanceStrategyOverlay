# import the clean_strategy function from clean_strategy.py
from clean_strategy import clean_strategy_text

# specify the path to the input .txt file
input_file = "raids.txt"

# read the contents of the input file
with open(input_file, "r") as file:
    strategies = file.readlines()

# iterate over each strategy in the file
for strategy in strategies:
    # remove any leading/trailing whitespace or newline characters
    strategy = strategy.strip()

    # call the clean_strategy function for each strategy
    clean_strategy_text(
        output_file=f"./data/cleaned_scraped/{strategy}.txt",
        input_file=f"./data/fetched_strategies/{strategy}.txt",
    )
