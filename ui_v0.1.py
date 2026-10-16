import streamlit as st

from app import analyze_log


# --------------------------------
# Streamlit Configuration
# --------------------------------

st.set_page_config(
    page_title="AI DevOps Log Analyzer",
    page_icon="🔍",
)


# --------------------------------
# Page Header
# --------------------------------

st.title("🔍 AI DevOps Log Analyzer")
st.caption("                   Created by Debasish")

st.write(
    "Upload a DevOps log and AI agent will "
    "analyze the failure and provide insights."
)


# --------------------------------
# Upload Log
# --------------------------------

uploaded_file = st.file_uploader(
    "Upload your DevOps log",
    type=["log", "txt"],
)


# --------------------------------
# Process Uploaded File
# --------------------------------

if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    log_content = uploaded_file.read().decode(
        "utf-8",
        errors="replace",
    )


    # --------------------------------
    # Show Uploaded Log
    # --------------------------------

    with st.expander("View uploaded log"):
        st.text(log_content)


    # --------------------------------
    # Analyze Log
    # --------------------------------

    if st.button("Analyze Log"):

        if not log_content.strip():

            st.warning(
                "The uploaded file is empty."
            )

            st.stop()


        with st.spinner(
            "Agent is analyzing the log..."
        ):

            result = analyze_log(log_content)


        # --------------------------------
        # Display Analysis
        # --------------------------------

        st.subheader("🤖 DevOps Log Analyzer")

        st.markdown(result)