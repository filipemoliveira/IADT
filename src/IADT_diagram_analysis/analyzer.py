import base64
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from models import ArchitectureComponent


load_dotenv()


PROMPT = """
You are an architecture diagram analyzer.

Analyze the provided architecture diagram and identify all visible
architecture components.

Return only a valid JSON array.

Each object must contain:
- name
- component_type

Allowed component_type values:
- user
- client
- web
- api
- service
- database
- storage
- queue
- identity
- external_system
- network
- other

Do not return explanations.
Do not use Markdown.
Do not wrap the response in a code block.
Return only valid JSON.
"""


def encode_image(image_path: str) -> str:
    """Converts an image to a Base64 data URL."""

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    extension = path.suffix.lower()

    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }

    mime_type = mime_types.get(extension)

    if mime_type is None:
        raise ValueError(
            "Unsupported image format. Use PNG, JPG, JPEG or WEBP."
        )

    image_bytes = path.read_bytes()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    return f"data:{mime_type};base64,{encoded_image}"


def analyze_diagram(
    image_path: str,
) -> list[ArchitectureComponent]:
    """Analyzes an architecture diagram using Azure OpenAI."""

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    if not endpoint:
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT was not found in the .env file."
        )

    if not api_key:
        raise ValueError(
            "AZURE_OPENAI_API_KEY was not found in the .env file."
        )

    if not deployment:
        raise ValueError(
            "AZURE_OPENAI_DEPLOYMENT was not found in the .env file."
        )

    client = OpenAI(
        base_url=endpoint,
        api_key=api_key,
    )

    image_data = encode_image(image_path)

    response = client.responses.create(
        model=deployment,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": PROMPT,
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data,
                    },
                ],
            }
        ],
    )

    response_text = response.output_text.strip()

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Azure OpenAI did not return valid JSON.\n"
            f"Response received:\n{response_text}"
        ) from error

    if not isinstance(data, list):
        raise ValueError(
            "Azure OpenAI response must be a JSON array."
        )

    components = []

    for item in data:
        if "name" not in item or "component_type" not in item:
            raise ValueError(
                "Each component must contain 'name' and "
                "'component_type'."
            )

        components.append(
            ArchitectureComponent(
                name=item["name"],
                component_type=item["component_type"],
            )
        )

    return components