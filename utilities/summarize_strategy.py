import sys
import argparse
from anthropic_api import call_anthropic_api
from prompts import (
    extraction_prompt,
    enhancement_prompt,
    compilation_prompt,
    final_check_and_polish,
    glossary_prompt,
)
from logging_config import configure_logging

logger = configure_logging()


def summarize_strategy_text(strategy_text, output_file=None):
    if not strategy_text:
        print("summarize_strategy_text: No strategy text provided.", file=sys.stderr)
        return

    try:
        print("Extracting boss information from the strategy text...", file=sys.stderr)
        extracted_info = process_strategy_text(
            strategy_text,
            "claude-3-5-sonnet-20240620",
            extraction_prompt,
            expected_output_tag="duty",
        )
        if extracted_info is None:
            return

        print("Enhancing the extracted information...", file=sys.stderr)
        enhanced_info = process_strategy_text(
            f"{glossary_prompt}{extracted_info}",
            "claude-3-5-sonnet-20240620",
            enhancement_prompt,
            expected_output_tag="duty",
        )
        if enhanced_info is None:
            return

        print("Compiling concise summary...", file=sys.stderr)
        compiled_summary = process_strategy_text(
            f"{glossary_prompt}{strategy_text}{enhanced_info}",
            "claude-3-opus-20240229",
            compilation_prompt,
            expected_output_tag="summary_text",
        )
        if compiled_summary is None:
            return

        print("Applying final check and polish...", file=sys.stderr)
        final_hud_display = process_strategy_text(
            f"{glossary_prompt}{strategy_text}{compiled_summary}",
            "claude-3-5-sonnet-20240620",
            final_check_and_polish,
            expected_output_tag="summary_text",
            include_output_tag=False,
        )
        if final_hud_display is None:
            return

        if final_hud_display:
            if output_file:
                try:
                    with open(output_file, "w") as file:
                        file.write(final_hud_display)
                    print(f"HUD-ready summary saved to {output_file}", file=sys.stderr)
                except IOError as e:
                    logger.exception(
                        f"Error occurred while saving HUD summary to file: {str(e)}"
                    )
                    print(
                        "Error occurred while saving HUD summary to file. Please check the logs for more details.",
                        file=sys.stderr,
                    )
            else:
                print(final_hud_display)
    except Exception as e:
        logger.exception(f"Error occurred while summarizing strategy text: {str(e)}")
        print(
            "Error occurred while summarizing strategy text. Please check the logs for more details.",
            file=sys.stderr,
        )


def process_strategy_text(
    strategy_text, model, prompt, expected_output_tag, include_output_tag=True
):
    try:
        processed_text = call_anthropic_api(
            prompt,
            strategy_text,
            expected_output_tag=expected_output_tag,
            model=model,
            include_output_tag=include_output_tag,
        )
        return processed_text
    except Exception as e:
        logger.exception(f"Error occurred while processing strategy text: {str(e)}")
        print(
            f"Error occurred while processing strategy text: {str(e)}", file=sys.stderr
        )
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Summarizes the cleaned strategy text using the Anthropic API."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s", "--strategy_text", nargs="?", help="Cleaned strategy text to summarize"
    )
    group.add_argument(
        "-i",
        "--input_file",
        help="Path to the file containing cleaned strategy text to summarize",
    )
    parser.add_argument(
        "-o", "--output_file", help="Path to save the summarized strategy text"
    )
    args = parser.parse_args()

    if args.strategy_text:
        summarize_strategy_text(args.strategy_text, args.output_file)
    elif args.input_file:
        try:
            with open(args.input_file, "r") as file:
                strategy_text = file.read()
            summarize_strategy_text(strategy_text, args.output_file)
        except IOError as e:
            logger.exception(f"Error occurred while reading input file: {str(e)}")
            print(
                "Error occurred while reading input file. Please check the logs for more details.",
                file=sys.stderr,
            )
    else:
        strategy_text = sys.stdin.read()
        summarize_strategy_text(strategy_text)


if __name__ == "__main__":
    main()
