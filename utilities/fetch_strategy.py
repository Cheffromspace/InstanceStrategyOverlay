import sys
import requests
import urllib.parse
import argparse
from bs4 import BeautifulSoup


def fetch_strategy(instance_name, output_file=None):
    encoded_instance_name = urllib.parse.quote(instance_name)
    url = f"https://ffxiv.consolegameswiki.com/wiki/{encoded_instance_name}"
    print(f"Fetching from {url}", file=sys.stderr)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the specific element(s) that contain the strategy text
        strategy_element = soup.select_one("div.mw-parser-output")

        if strategy_element:
            strategy_text = strategy_element.get_text(strip=True)
            if output_file:
                try:
                    with open(output_file, "w") as file:
                        file.write(strategy_text)
                except IOError as e:
                    print(f"Error saving strategy to file: {e}", file=sys.stderr)
        else:
            strategy_text = "Strategy not found"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching strategy: {e}", file=sys.stderr)
        strategy_text = "Strategy not found"

    return strategy_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetches the strategy text for a given FFXIV instance from consolegameswiki.com."
    )
    parser.add_argument("instance_name", nargs="?", help="Name of the FFXIV instance")
    parser.add_argument(
        "-o", "--output_file", type=str, help="Path to save the strategy text"
    )
    args = parser.parse_args()

    if not args.instance_name:
        instance_name = sys.stdin.read().strip()
    else:
        instance_name = args.instance_name

    strategy_text = fetch_strategy(instance_name, output_file=args.output_file)
    print(strategy_text)
