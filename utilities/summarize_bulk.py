# import the clean_strategy function from clean_strategy.py
from summarize_strategy import summarize_strategy_text

# specify the path to the input .txt file
input_file = "raids.txt"

# read the contents of the input file
with open(input_file, "r") as file:
    strategies = file.readlines()

# iterate over each strategy in the file
for strategy in strategies:
    # remove any leading/trailing whitespace or newline characters
    strategy = strategy.strip()
    # get the cleaned summary of the strategy
    # call the clean_strategy function for each strategy
    try:
        with open(f"./data/cleaned_scraped/{strategy}.txt", "r") as file:
            strategy_text = file.read()

        summarize_strategy_text(
            strategy_text=strategy_text,
            output_file=f"strategies/{strategy}.txt",
        )
    except Exception as e:
        print(f"Error summarizing strategy {strategy}: {e}")
