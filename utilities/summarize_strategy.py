import sys
import argparse
from anthropic_api import call_anthropic_api
from prompts import summary_system_prompt


def summarize_strategy_text(strategy_text, output_file=None):
    system_prompt = summary_system_prompt
    summary_text = call_anthropic_api(
        system_prompt, strategy_text, expected_tag="summary_text"
    )

    if summary_text is not None:
        if output_file:
            with open(output_file, "w") as file:
                file.write(summary_text)
                print(f"Summary saved to {output_file}", file=sys.stderr)
                print(summary_text)
        else:
            print(summary_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Summarizes the cleaned strategy text using the Anthropic API."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s", "--strategy_text", nargs="?", help="Cleaned strategy text to summarize"
    )
    group.add_argument(
        "-i", "--input_file", help="File containing cleaned strategy text to summarize"
    )
    parser.add_argument(
        "-o", "--output_file", help="Save path for the summarized strategy text"
    )
    args = parser.parse_args()

    if args.strategy_text:
        summary = summarize_strategy_text(args.strategy_text)
    if args.input_file:
        with open(args.input_file, "r") as file:
            strategy_text = file.read()
            summary = summarize_strategy_text(strategy_text, args.output_file)
    else:
        strategy_text = sys.stdin.read()
        summary = summarize_strategy_text(strategy_text)

    print(summary)
