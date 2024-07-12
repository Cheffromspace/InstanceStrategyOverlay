import unittest
from unittest.mock import patch, MagicMock
from anthropic_api import (
    call_anthropic_api,
    extract_response_text,
    extract_error_message,
)
from clean_strategy import clean_strategy_text
from fetch_strategy import fetch_strategy
from summarize_strategy import process_strategy_text, summarize_strategy_text


class TestAnthropicAPI(unittest.TestCase):
    @patch("anthropic.Anthropic")
    def test_call_anthropic_api(self, mock_anthropic):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content = [
            MagicMock(text="<output_tag>Response Text</output_tag>")
        ]

        response = call_anthropic_api("System Prompt", "User Message", "output_tag")

        self.assertEqual(response, "<output_tag>Response Text</output_tag>")

    def test_extract_response_text(self):
        response = "<output_tag>Extracted Text</output_tag>"
        extracted_text = extract_response_text(response, "output_tag")
        self.assertEqual(extracted_text, "<output_tag>Extracted Text</output_tag>")

    def test_extract_error_message(self):
        response = "<error>Error Message</error>"
        error_message = extract_error_message(response)
        self.assertEqual(error_message, "Error Message")


class TestCleanStrategy(unittest.TestCase):
    @patch("clean_strategy.call_anthropic_api")
    def test_clean_strategy_text(self, mock_call_anthropic_api):
        mock_call_anthropic_api.return_value = (
            "<cleaned_strategy_text>Cleaned Strategy Text</cleaned_strategy_text>"
        )
        cleaned_text = clean_strategy_text("Strategy Text")
        self.assertEqual(cleaned_text, "Cleaned Strategy Text")


class TestFetchStrategy(unittest.TestCase):
    @patch("requests.get")
    def test_fetch_strategy(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<div class='mw-parser-output'>Strategy Text</div>"
        mock_get.return_value = mock_response

        strategy_text = fetch_strategy("Instance Name")
        self.assertEqual(strategy_text, "Strategy Text")


class TestSummarizeStrategy(unittest.TestCase):
    @patch("summarize_strategy.call_anthropic_api")
    def test_process_strategy_text(self, mock_call_anthropic_api):
        mock_call_anthropic_api.return_value = (
            "<output_tag>Processed Strategy Text</output_tag>"
        )
        processed_text = process_strategy_text(
            "Strategy Text", "Model", "Prompt", "output_tag"
        )
        self.assertEqual(
            processed_text, "<output_tag>Processed Strategy Text</output_tag>"
        )

    @patch("summarize_strategy.process_strategy_text")
    def test_summarize_strategy_text(self, mock_process_strategy_text):
        mock_process_strategy_text.side_effect = [
            "<boss_info>Boss Info</boss_info>",
            "<bullet_points>Bullet Points</bullet_points>",
            "<formatted_text>Formatted Text</formatted_text>",
            "<summary_text>Summary Text</summary_text>",
        ]
        summarize_strategy_text("Cleaned Strategy Text")
        self.assertEqual(mock_process_strategy_text.call_count, 4)


if __name__ == "__main__":
    unittest.main()
