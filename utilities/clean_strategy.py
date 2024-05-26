import os
import sys
import argparse
from anthropic_api import call_anthropic_api


def clean_strategy_text(strategy_text=None, input_file=None, output_file=None):
    if input_file:
        try:
            with open(input_file, "r") as f:
                strategy_text = f.read()
        except IOError as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            return

    cleanup_scraped_system_prompt = """
    You are a helpful AI, tasked with cleaning up text from scraped strategy and quest guides for the game Final Fantasy 14. Your task is to remove unnecessary content while preserving the actual guide content:
    """

    cleanup_scraped_text_prompt = f"""
    Here is the text scraped from a Final Fantasy 14 instance guide:

    <scraped_text>
    {strategy_text}
    </scraped_text>

    Your task is to extract only the strategy text from this scraped content. Remove things like links, lore, loot tables, images, achievements, and other non-strategy information. It's critical that you do not alter any of the actual strategy content itself.
    The strategy text will contain the names of bosses, abilities, descriptions of abilities, mechanics, and other notes relevant to defeating the instance. DO NOT modify any of this information. Only remove non-strategy content.

    Output the extracted strategy text inside <cleaned_strategy_text>...</cleaned_strategy_text> tags.

    If there are any issues with the input text or if you are unable to generate a cleaned/summarized version, do not output the requested tags. Instead, provide an error message wrapped in <error>...</error> tags explaining the issue.
    """

    cleaned_strategy_text = call_anthropic_api(
        system_prompt=cleanup_scraped_system_prompt,
        user_message=cleanup_scraped_text_prompt,
        model="claude-3-sonnet-20240229",
        expected_tag="cleaned_strategy_text",
    )

    if output_file:
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w") as f:
                f.write(cleaned_strategy_text)
            print(f"Cleaned strategy text saved to {output_file}", file=sys.stderr)
        except IOError as e:
            print(f"Error saving cleaned strategy text to file: {e}", file=sys.stderr)
    else:
        print(cleaned_strategy_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cleans the scraped strategy text using the Anthropic API."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--input_file",
        type=str,
        help="Input file path containing the strategy text to clean.",
    )
    group.add_argument("-s", "--strategy_text", help="Strategy text to clean.")
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        help="Output path to save the cleaned strategy text. If not provided, the cleaned strategy text will be printed to stdout.",
    )
    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, "r") as f:
            strategy_text = f.read()
    elif args.strategy_text:
        strategy_text = args.strategy_text
    else:
        strategy_text = sys.stdin.read()

    cleaned_strategy_text = clean_strategy_text(
        strategy_text, input_file=args.input_file, output_file=args.output_file
    )

    if cleaned_strategy_text:
        print(cleaned_strategy_text)
