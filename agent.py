import asyncio

from azure.ai.agentserver.responses import (
    CreateResponse,
    ResponseContext,
    ResponsesAgentServerHost,
    TextResponse,
)

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from config import (
    FOUNDRY_PROJECT_ENDPOINT,
    FOUNDRY_MODEL,
)


# ---------------------------------------------------------
# Foundry client
# ---------------------------------------------------------

project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

openai_client = project.get_openai_client()


# ---------------------------------------------------------
# Agent instructions
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are an experienced DevOps and SRE engineer.

Analyze the provided DevOps log.

Return your analysis using exactly these sections:

1. Error Summary
2. Likely Root Cause
3. Possible Causes
4. Recommended Remediation
5. Verification Steps

Only use information supported by the log.

Do not invent facts.

If the log does not contain enough information,
clearly state what additional information is required.
"""


# ---------------------------------------------------------
# Agent logic
# ---------------------------------------------------------

async def analyze_log(log_content: str) -> str:

    user_prompt = f"""
Analyze the following DevOps log:

---------------- LOG START ----------------

{log_content}

----------------- LOG END -----------------

Provide the requested DevOps analysis.
"""

    response = openai_client.responses.create(
        model=FOUNDRY_MODEL,
        instructions=SYSTEM_PROMPT,
        input=user_prompt,
    )

    return response.output_text


# ---------------------------------------------------------
# Foundry Hosted Agent
# ---------------------------------------------------------

app = ResponsesAgentServerHost()


@app.response_handler
async def handler(
    request: CreateResponse,
    context: ResponseContext,
    _cancellation_signal: asyncio.Event,
):

    user_input = await context.get_input_text() or ""

    result = await analyze_log(user_input)

    return TextResponse(
        context,
        request,
        text=result,
    )


# ---------------------------------------------------------
# Start hosted agent
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run()