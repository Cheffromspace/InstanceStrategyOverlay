import anthropic
import sys
from logging_config import configure_logging

logger = configure_logging()


def call_anthropic_api(
    system_prompt,
    user_message,
    expected_tag,
    include_tag=True,
    model="claude-3-opus-20240229",
):
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
    return extract_response_text(response_text, expected_tag, include_tag=include_tag)


def extract_response_text(response, expected_tag, include_tag=True):
    start_tag = f"<{expected_tag}>"
    end_tag = f"</{expected_tag}>"
    start_index = response.find(start_tag)
    end_index = response.find(end_tag)
    if start_index != -1 and end_index != -1:
        if include_tag:
            end_index += len(end_tag)
        else:
            start_index += len(start_tag)
        extracted_text = response[start_index:end_index].strip()
        return extracted_text
    else:
        error_message = extract_error_message(response)
        if error_message:
            logger.error(f"Error in API response: {error_message}")
            print(f"Error in API response: {error_message}", file=sys.stderr)
            import traceback

            traceback.print_exc()
        else:
            logger.error(
                f"Expected tag <{expected_tag}> not found in the API response. \n Response: [{response}]"
            )
            print(
                f"Expected tag <{expected_tag}> not found in the API response. \n Response: [{response}]",
                file=sys.stderr,
            )


def extract_error_message(response):
    start_tag = "<error>"
    end_tag = "</error>"
    start_index = response.find(start_tag)
    end_index = response.find(end_tag)

    if start_index != -1 and end_index != -1:
        start_index += len(start_tag)
        error_message = response[start_index:end_index].strip()
        return error_message
    else:
        return None
