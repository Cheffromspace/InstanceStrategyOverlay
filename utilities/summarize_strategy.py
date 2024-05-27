import sys
import argparse
from anthropic_api import call_anthropic_api
from prompts import (
    extract_bosses_and_phases_prompt,
    generate_bullet_points_prompt,
    add_emojis_and_formatting_prompt,
    compile_summary_prompt,
)


def process_strategy_text(
    strategy_text, model, prompt, expected_tag, include_tag=True, dev_debug=False
):
    try:
        processed_text = call_anthropic_api(
            prompt,
            strategy_text,
            expected_tag=expected_tag,
            model=model,
            include_tag=include_tag,
        )
        return processed_text
    except Exception as e:
        print(
            f"Error occurred while processing strategy text: {str(e)}", file=sys.stderr
        )
        if dev_debug:
            import traceback

            traceback.print_exc()
        return None


def summarize_strategy_text(strategy_text, output_file=None, dev_debug=False):
    try:
        extracted_text = process_strategy_text(
            strategy_text,
            "claude-3-sonnet-20240229",
            extract_bosses_and_phases_prompt,
            "duty",
        )
        if not extracted_text:
            return

        bullet_points = process_strategy_text(
            extracted_text,
            "claude-3-sonnet-20240229",
            generate_bullet_points_prompt,
            "duty",
        )
        if not bullet_points:
            return

        formatted_text = process_strategy_text(
            bullet_points,
            "claude-3-sonnet-20240229",
            add_emojis_and_formatting_prompt,
            "duty",
        )
        if not formatted_text:
            return

        user_message = f"""
        {strategy_text}
        {formatted_text}
        Let's think this through step by step to ensure we have a comprehensive summary of the strategy guide.
        """
        summary_text = process_strategy_text(
            user_message,
            "claude-3-opus-20240229",
            compile_summary_prompt,
            "summary_text",
            include_tag=False,
        )

        if summary_text:
            if output_file:
                try:
                    with open(output_file, "w") as file:
                        file.write(summary_text)
                    print(f"Summary saved to {output_file}", file=sys.stderr)
                except IOError as e:
                    print(
                        f"Error occurred while saving summary to file: {str(e)}",
                        file=sys.stderr,
                    )
            else:
                print(summary_text)
    except Exception as e:
        print(
            f"Error occurred while summarizing strategy text: {str(e)}", file=sys.stderr
        )
        if dev_debug:
            import traceback

            traceback.print_exc()


def main():
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
    parser.add_argument(
        "--dev_debug", help="Save path for the summarized strategy text"
    )
    args = parser.parse_args()

    if args.strategy_text:
        summarize_strategy_text(args.strategy_text, args.output_file, args.dev_debug)
    elif args.input_file:
        try:
            with open(args.input_file, "r") as file:
                strategy_text = file.read()
            summarize_strategy_text(strategy_text, args.output_file, args.dev_debug)
        except IOError as e:
            print(f"Error occurred while reading input file: {str(e)}", file=sys.stderr)
    else:
        strategy_text = sys.stdin.read()
        summarize_strategy_text(strategy_text)


if __name__ == "__main__":
    main()
