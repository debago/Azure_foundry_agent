import requests
from azure.identity import DefaultAzureCredential

from config import FOUNDRY_HOSTED_AGENT_ENDPOINT


credential = DefaultAzureCredential(
    exclude_interactive_browser_credential=True
)


def analyze_log(log_content: str) -> str:

    token = credential.get_token(
        "https://ai.azure.com/.default"
    )

    headers = {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json",
    }

    body = {
        "input": log_content
    }

    response = requests.post(
        FOUNDRY_HOSTED_AGENT_ENDPOINT,
        headers=headers,
        json=body,
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    for item in result.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return content.get("text", "")

    return "No text response returned by the hosted agent."