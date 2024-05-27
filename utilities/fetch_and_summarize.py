import sys
import argparse
from fetch_strategy import fetch_strategy
from clean_strategy import clean_strategy_text
from summarize_strategy import summarize_strategy_text


def fetch_and_summarize(instance_name, save_to_repo=False):
    strategy_text = fetch_strategy(instance_name)

    if strategy_text == "Strategy not found":
        return "Error: Strategy not found"

    cleaned_strategy_text = clean_strategy_text(
        strategy_text,
    )
    summary = summarize_strategy_text(cleaned_strategy_text)

    if summary is None:
        return "Error: Summary not found"

    if save_to_repo:
        try:
            with open(f"strategies/{instance_name}.html", "w") as f:
                f.write(summary)
        except IOError as e:
            print(f"Error saving summary to file: {e}")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetches the strategy text for a given FFXIV instance from consolegameswiki.com."
    )
    parser.add_argument("--instance", help="Name of the FFXIV instance")
    parser.add_argument(
        "--save", action="store_true", help="Save the strategy to the repo"
    )
    args = parser.parse_args()

    if args.instance:
        instance = args.instance
    else:
        instance = sys.stdin.read().strip()

    strategy_text = fetch_and_summarize(instance, args.save)
    print(strategy_text)
