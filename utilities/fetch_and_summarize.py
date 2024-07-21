import sys
import argparse
import os
from fetch_strategy import fetch_strategy
from clean_strategy import clean_strategy_text
from summarize_strategy import summarize_strategy_text


def fetch_and_summarize(instance_name, save_to_repo=False):
    if save_to_repo:
        script_path = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(script_path))
        data_dir = os.path.join(project_root, "data")
        strategy_text = fetch_strategy(
            instance_name,
            output_file=f"{data_dir}/fetched/{instance_name}.txt",
        )
        print(f"Fetched strategy text for {instance_name}")
        print(strategy_text)
        cleaned_strategy_text = clean_strategy_text(
            strategy_text,
            output_file=f"{data_dir}/cleaned/{instance_name}.txt",
        )

        summarize_strategy_text(
            cleaned_strategy_text,
            output_file=f"{data_dir}/strategies/{instance_name}.html",
        )
    else:
        strategy_text = fetch_strategy(instance_name)
        cleaned_strategy_text = clean_strategy_text(strategy_text)
        summarize_strategy_text(cleaned_strategy_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetches the strategy text for a given FFXIV instance from consolegameswiki.com."
    )
    parser.add_argument("--instance", help="Name of the FFXIV instance")
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the fetched, cleaned, and summarized strategy text to the repository. If not specified, the strategy text will be printed to the console.",
    )
    args = parser.parse_args()

    if args.instance:
        instance = args.instance
    else:
        instance = sys.stdin.read().strip()

    strategy_text = fetch_and_summarize(instance, args.save)
    print(strategy_text)
