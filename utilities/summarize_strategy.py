import sys
import argparse
from anthropic_api import call_anthropic_api
from prompts import (
    extract_bosses_and_phases_prompt,
    generate_bullet_points_prompt,
    add_emojis_and_formatting_prompt,
    compile_summary_prompt,
)


def extract_bosses_and_phases(cleaned_strategy_text):
    system_prompt = extract_bosses_and_phases_prompt
    extracted_text = call_anthropic_api(
        system_prompt,
        cleaned_strategy_text,
        expected_tag="duty",
        model="claude-3-sonnet-20240229",
    )
    return extracted_text


def generate_bullet_points(duty_text):
    system_prompt = generate_bullet_points_prompt
    bullet_points = call_anthropic_api(
        system_prompt, duty_text, expected_tag="duty", model="claude-3-sonnet-20240229"
    )
    return bullet_points


def add_emojis_and_formatting(duty_text):
    system_prompt = add_emojis_and_formatting_prompt
    formatted_text = call_anthropic_api(
        system_prompt, duty_text, expected_tag="duty", model="claude-3-sonnet-20240229"
    )
    return formatted_text


def compile_summary(bullet_points_text, cleaned_strategy_text):
    user_message = f"""
    {cleaned_strategy_text}
    {bullet_points_text}
    Let's think this through step by step to ensure we have a comprehensive summary of the strategy guide.
    """

    summary_text = call_anthropic_api(
        compile_summary_prompt,
        user_message,
        expected_tag="summary_text",
        model="claude-3-opus-20240229",
        include_tag=False,
    )
    return summary_text


def summarize_strategy_text(strategy_text, output_file=None):
    extracted_text = extract_bosses_and_phases(strategy_text)
    bullet_points = generate_bullet_points(extracted_text)
    formatted_text = add_emojis_and_formatting(bullet_points)
    summary_text = compile_summary(formatted_text, strategy_text)

    if summary_text is not None:
        if output_file:
            with open(output_file, "w") as file:
                file.write(summary_text)
                print(f"Summary saved to {output_file}", file=sys.stderr)
        else:
            print(summary_text)
        return


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
