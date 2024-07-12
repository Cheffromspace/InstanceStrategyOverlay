import anthropic
from logging_config import configure_logging

logger = configure_logging()


def call_anthropic_api(
    system_prompt,
    user_message,
    expected_output_tag,
    include_output_tag=True,
    model="claude-3-5-sonnet-20240620",
):
    """
    Calls the Anthropic API to generate a response based on the provided prompts.

    Args:
        system_prompt (str): The system prompt that sets the context for the conversation.
        user_message (str): The user message to send to the API.
        expected_output_tag (str): The tag that wraps the expected output text in the API response.
        include_output_tag (bool, optional): Whether to include the output tag in the extracted response text.
            Defaults to True.
        model (str, optional): The name of the Anthropic model to use. Defaults to "claude-3-opus-20240229".

    Returns:
        str: The extracted response text from the API.

    Raises:
        ValueError: If an error occurs in the API response or if the expected output tag is not found.
    """
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_message,
                    }
                ],
            }
        ],
    )
    response_text = message.content[0].text
    print(response_text)
    return extract_response_text(
        response_text, expected_output_tag, include_output_tag=include_output_tag
    )


def extract_response_text(response, expected_output_tag, include_output_tag=True):
    """
    Extracts the response text from the API response based on the specified expected output tag.
    Args:
        response (str): The API response text.
        expected_output_tag (str): The tag that wraps the expected output text in the API response.
        include_output_tag (bool, optional): Whether to include the output tag in the extracted response text.
            Defaults to True.
    Returns:
        str: The extracted response text.
    Raises:
        ValueError: If an error occurs in the API response or if the expected output tag is not found.
    """

    def extract_tag_content(tag):
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start_index = response.find(start_tag)
        end_index = response.find(end_tag)
        if start_index != -1 and end_index != -1:
            if include_output_tag:
                return response[start_index : end_index + len(end_tag)].strip()
            else:
                return response[start_index + len(start_tag) : end_index].strip()
        return None

    extracted_text = extract_tag_content(expected_output_tag)
    if extracted_text:
        return extracted_text

    error_message = extract_tag_content("error")
    if error_message:
        logger.error(f"Error in API response: {error_message}")
        raise ValueError(f"Error in API response: {error_message}")
    else:
        logger.error(
            f"Expected tag <{expected_output_tag}> not found in the API response. \n Response: [{response}]"
        )
        raise ValueError(
            f"Expected tag <{expected_output_tag}> not found in the API response."
        )
