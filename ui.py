
import streamlit as st

from app import analyze_log


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI DevOps Log Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .app-title {
            font-size: 32px;
            font-weight: 700;
            color: #172033;
            margin-bottom: 0;
        }

        .app-subtitle {
            color: #687386;
            font-size: 15px;
            margin-top: 5px;
        }

        .creator {
            text-align: right;
            color: #687386;
            font-size: 13px;
            padding-top: 8px;
        }

        .creator-name {
            font-weight: 600;
            color: #3b4658;
            font-size: 15px;
        }

        .section-title {
            font-size: 19px;
            font-weight: 650;
            color: #202938;
            margin-top: 20px;
        }

        .section-description {
            color: #737d8d;
            font-size: 14px;
            margin-bottom: 15px;
        }

        .footer {
            text-align: center;
            color: #8a93a2;
            font-size: 12px;
            margin-top: 40px;
            padding-top: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
title_col, creator_col = st.columns([5, 1])

with title_col:

    st.markdown(
        '<div class="app-title">🔍 AI DevOps Log Analyzer</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-subtitle">'
        'Intelligent DevOps troubleshooting powered by Microsoft Foundry and AI.'
        '</div>',
        unsafe_allow_html=True,
    )


with creator_col:

    st.markdown(
        '<div class="creator">'
        'Created by<br>'
        '<span class="creator-name">Debasish</span>'
        '</div>',
        unsafe_allow_html=True,
    )


st.divider()


# ---------------------------------------------------------
# Upload section
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📄 Upload DevOps Log</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Upload a pipeline, deployment, ADF, Docker, '
    'or other DevOps log file for AI-powered analysis.'
    '</div>',
    unsafe_allow_html=True,
)


uploaded_file = st.file_uploader(
    "Select a log file",
    type=["log", "txt"],
)


# ---------------------------------------------------------
# Process uploaded file
# ---------------------------------------------------------
if uploaded_file:

    log_content = uploaded_file.read().decode(
        "utf-8",
        errors="replace",
    )

    st.success(
        f"File uploaded successfully: {uploaded_file.name}"
    )

    # -----------------------------------------------------
    # Preview
    # -----------------------------------------------------
    with st.expander("📋 View uploaded log"):

        st.code(
            log_content,
            language="text",
        )


    # -----------------------------------------------------
    # Analyze
    # -----------------------------------------------------
    if st.button(
        "🤖 Analyze Log",
        type="primary",
        use_container_width=True,
    ):

        if not log_content.strip():

            st.warning(
                "The uploaded file is empty."
            )

            st.stop()


        with st.spinner(
            "AI DevOps Agent is analyzing the log..."
        ):

            try:

                result = analyze_log(
                    log_content
                )

                st.divider()

                st.subheader(
                    "🤖 AI DevOps Analysis"
                )

                st.markdown(
                    result
                )

            except Exception as e:

                st.error(
                    f"Unable to analyze the log: {str(e)}"
                )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.divider()

st.caption(
    "AI DevOps Log Analyzer • Microsoft Foundry • "
    "Intelligent DevOps Troubleshooting"
)

