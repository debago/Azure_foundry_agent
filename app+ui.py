import streamlit as st

from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential

from config import (
    FOUNDRY_PROJECT_ENDPOINT,
    FOUNDRY_MODEL,
)


# --------------------------------
# Microsoft Foundry Client
# --------------------------------

project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=AzureCliCredential(process_timeout=60),
)

openai_client = project.get_openai_client()


# --------------------------------
# Streamlit UI
# --------------------------------

st.set_page_config(
    page_title="AI DevOps Log Analyzer",
    page_icon="🔍",
)

st.title("🔍 AI DevOps Log Analyzer")

st.write(
    "Upload a DevOps log and use Microsoft Foundry "
    "to analyze the failure."
)


# --------------------------------
# Upload Log
# --------------------------------

uploaded_file = st.file_uploader(
    "Upload your DevOps log",
    type=["log", "txt"],
)


if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    log_content = uploaded_file.read().decode(
        "utf-8",
        errors="replace",
    )

    # Show uploaded log
    with st.expander("View uploaded log"):
        st.text(log_content)

    # --------------------------------
    # Analyze
    # --------------------------------

    if st.button("Analyze Log"):

        if not log_content.strip():

            st.warning(
                "The uploaded file is empty."
            )

            st.stop()

        system_prompt = """
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

        user_prompt = f"""
Analyze the following DevOps log:

---------------- LOG START ----------------

{log_content}

----------------- LOG END -----------------

Provide the requested DevOps analysis.
"""

        with st.spinner(
            "Agent is analyzing the log..."
        ):

            response = openai_client.responses.create(
                model=FOUNDRY_MODEL,
                instructions=system_prompt,
                input=user_prompt,
            )

        st.subheader("🤖 DevOps Log Analyzer")

        st.markdown(
            response.output_text
        )