import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from graph.workflow import app
from retrieval.retriever import retrieve


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="V-RAG",
    page_icon="§",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================
#
# Design tokens (dark)
# --------------------
# Background   #14161C   (cool charcoal, not pure black)
# Surface      #1B1E26
# Surface alt  #20232C   (nested surfaces, evidence blocks)
# Border       #2C3039
# Text primary #E7E8EC
# Text muted   #90959F
# Responder    #6FA0D6   (steel blue  — builds the case)
# Prosecutor   #C97C74   (muted brick — tests the case)
# Judge        #9A8AC9   (muted plum  — rules on the case)
# Accept       #6EB088   (sage)
# Revise       #D6A15B   (amber)
# Display face  "Source Serif 4"  — case-file authority, used sparingly
# Body face     "Inter"           — neutral, high legibility
# Mono face     "IBM Plex Mono"   — ids, chunks, queries, docket marks
#
st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* ========================================================
       GLOBAL
    ======================================================== */

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .stApp {
        background: #14161C;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    body, p, li, span, div {
        color: #E7E8EC;
    }

    hr {
        border: none;
        border-top: 1px solid #2C3039;
        margin: 2.2rem 0 !important;
    }


    /* ========================================================
       HEADER
    ======================================================== */


    h1 {
        font-family: 'Source Serif 4', Georgia, serif !important;
        font-size: 2.6rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        letter-spacing: -0.02em;
        color: #F3F4F6;
        margin-bottom: 0.3rem !important;
        line-height: 1.1;
    }

    .app-subtitle {
        color: #90959F;
        font-size: 1rem;
        font-weight: 400;
        text-align: center;
        margin-bottom: 2.4rem;
        padding-bottom: 2.2rem;
        border-bottom: 1px solid #2C3039;
    }


    /* ========================================================
       SECTION HEADINGS
    ======================================================== */

    h2 {
        font-family: 'Source Serif 4', Georgia, serif !important;
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.015em;
        color: #F3F4F6;
        margin-top: 1.6rem !important;
        margin-bottom: 0.9rem !important;
    }

    h3 {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #F3F4F6;
    }

    .section-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #90959F;
        margin-bottom: 0.7rem;
    }


    /* ========================================================
       FINAL ANSWER
    ======================================================== */

    .final-answer-label {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.45rem;
        font-weight: 700;
        color: #F3F4F6;
        letter-spacing: -0.015em;
        margin-bottom: 0.9rem;
    }

    .final-answer-box {
        padding: 1.5rem 1.7rem;
        border: 1px solid #2C3039;
        border-left: 3px solid #6FA0D6;
        border-radius: 4px;
        background: #1B1E26;
        color: #E7E8EC;
        line-height: 1.75;
        font-size: 1.04rem;
    }

    /* ========================================================
    EXECUTION TIMELINE
    ======================================================== */

    .timeline {
        margin: 1rem 0 0.5rem 0;
    }

    .timeline-round-group {
        margin-bottom: 1.6rem;
    }

    .timeline-round {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #90959F;
        margin: 0 0 0.9rem 0;
    }

    .timeline-row {
        display: flex;
        align-items: flex-start;
        flex-wrap: nowrap;
        overflow-x: auto;
        padding-bottom: 0.4rem;
    }

    .timeline-item {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        position: relative;
        flex: 0 0 auto;
        min-width: 150px;
        max-width: 190px;
    }

    .timeline-connector {
        flex: 0 0 32px;
        height: 1px;
        margin-top: 9px;
        background: #2C3039;
    }

    .timeline-dot {
        width: 17px;
        height: 17px;
        border-radius: 50%;
        flex-shrink: 0;
        border: 2px solid #6B707B;
        background: #14161C;
        position: relative;
        z-index: 1;
    }

    .timeline-dot.complete {
        border-color: #6EB088;
        background: #6EB088;
    }

    .timeline-dot.investigation {
        border-color: #D6A15B;
        background: #D6A15B;
    }

    .timeline-dot.revise {
        border-color: #D6A15B;
        background: #D6A15B;
    }

    .timeline-dot.accept {
        border-color: #6EB088;
        background: #6EB088;
    }

    .timeline-content {
        padding-top: 0.5rem;
        padding-right: 0.8rem;
    }

    .timeline-agent {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1rem;
        font-weight: 700;
        color: #E7E8EC;
        white-space: nowrap;
    }

    .timeline-status {
        font-size: 0.78rem;
        color: #90959F;
        margin-top: 0.15rem;
    }

    .timeline-status.accept {
        color: #8FCBA8;
    }

    .timeline-status.revise {
        color: #E3BC85;
    }

    .timeline-status.investigation {
        color: #E3BC85;
    }


    /* ========================================================
       AGENT CARDS
    ======================================================== */

    .agent-block {
        background: #1B1E26;
        border: 1px solid #2C3039;
        border-radius: 6px;
        padding: 1.5rem 1.6rem 1.7rem 1.6rem;
        height: 100%;
    }

    .agent-eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.14em;
        margin-bottom: 0.35rem;
    }

    .agent-header {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: -0.015em;
        margin-bottom: 0.4rem;
    }

    .responder-eyebrow { color: #6FA0D6; }
    .prosecutor-eyebrow { color: #C97C74; }
    .judge-eyebrow { color: #9A8AC9; }

    .responder-header { color: #A9CBEB; }
    .prosecutor-header { color: #E3AFA9; }
    .judge-header { color: #C5B8E4; }

    .agent-description {
        color: #90959F;
        font-size: 0.9rem;
        line-height: 1.55;
        margin-bottom: 1.3rem;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid #262A33;
    }

    .subheading {
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: #90959F;
        margin-top: 0.9rem;
        margin-bottom: 0.6rem;
    }


    /* ========================================================
       METRICS
    ======================================================== */

    div[data-testid="stMetric"] {
        padding: 1rem 1.1rem;
        border: 1px solid #2C3039;
        border-radius: 6px;
        background: #1B1E26;
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #90959F;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #F3F4F6;
    }


    /* ========================================================
       EXPANDERS
    ======================================================== */

    div[data-testid="stExpander"] {
        border: 1px solid #2C3039;
        border-radius: 6px;
        overflow: hidden;
        background: #1B1E26;
    }

    div[data-testid="stExpander"] summary {
        font-weight: 500;
        font-size: 0.92rem;
        color: #E7E8EC;
    }


    /* ========================================================
       QUESTION INPUT
    ======================================================== */

    textarea {
        border-radius: 6px !important;
        border: 1px solid #2C3039 !important;
        font-size: 1rem !important;
        background: #1B1E26 !important;
        color: #E7E8EC !important;
    }

    textarea:focus {
        border-color: #6FA0D6 !important;
        box-shadow: 0 0 0 1px #6FA0D6 !important;
    }

    textarea::placeholder {
        color: #6B707B !important;
    }


    /* ========================================================
       RUN BUTTON
    ======================================================== */

    .stButton > button {
        border-radius: 5px;
        font-weight: 600;
        letter-spacing: 0.01em;
        min-height: 2.75rem;
        font-size: 0.92rem;
        color: #14161C;
    }


    /* ========================================================
       EVIDENCE REFERENCES
    ======================================================== */

    .evidence-reference {
        padding: 0.65rem 0.85rem;
        border: 1px solid #2C3039;
        border-left: 2px solid #6FA0D6;
        border-radius: 4px;
        margin-top: 0.5rem;
        margin-bottom:1rem;
        background: #20232C;
    }

    .evidence-source {
        font-size: 0.82rem;
        font-weight: 600;
        color: #E7E8EC;
        word-break: break-word;
    }

    .evidence-chunk {
        font-family: 'IBM Plex Mono', monospace;
        color: #90959F;
        font-size: 0.72rem;
        margin-top: 0.2rem;
    }


    /* ========================================================
       RISK LABELS
    ======================================================== */

    .risk-label {
        display: inline-block;
        padding: 0.22rem 0.6rem;
        border-radius: 3px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.07em;
        text-transform: uppercase;
    }

    .risk-low {
        background: rgba(110, 176, 136, 0.14);
        color: #8FCBA8;
    }

    .risk-medium {
        background: rgba(214, 161, 91, 0.14);
        color: #E3BC85;
    }

    .risk-high {
        background: rgba(201, 124, 116, 0.16);
        color: #E3AFA9;
    }


    /* ========================================================
       JUDGE VERDICT SEAL
       (signature element — a stamped ruling rather than a badge)
    ======================================================== */

    .verdict-seal {
        display: inline-block;
        padding: 0.9rem 1.3rem;
        border: 1px solid currentColor;
        border-radius: 3px;
        position: relative;
    }

    .verdict-seal::before {
        content: "";
        position: absolute;
        top: 3px; left: 3px; right: 3px; bottom: 3px;
        border: 1px solid currentColor;
        border-radius: 2px;
        opacity: 0.4;
        pointer-events: none;
    }

    .verdict-seal-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        opacity: 0.8;
        margin-bottom: 0.15rem;
    }

    .verdict-seal-value {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.55rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }

    .verdict-accept { color: #6EB088; }
    .verdict-revise { color: #D6A15B; }


    /* ========================================================
       PIPELINE DETAILS
    ======================================================== */

    .pipeline-heading {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #F3F4F6;
        margin-bottom: 1.1rem;
    }


    /* ========================================================
       STREAMLIT ALERT BOXES (warning / success / info)
    ======================================================== */

    div[data-testid="stAlert"] {
        background: #1B1E26;
    }

    div[data-testid="stAlert"] p {
        color: #E7E8EC;
    }


    /* ========================================================
       CODE BLOCKS
    ======================================================== */

    .stCodeBlock, code {
        background: #20232C !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

def render_timeline(events, placeholder):

    # NOTE: every fragment below is built with zero leading whitespace.
    # Streamlit's markdown renderer treats any line indented by 4+ spaces
    # as a literal code block, so indenting these strings (as Python
    # code style would normally suggest) causes the HTML to be displayed
    # as raw text instead of being rendered.

    parts = ['<div class="timeline">']

    current_round = None
    round_open = False

    for event in events:

        round_number = event["round"]

        if round_number != current_round:

            if round_open:
                parts.append("</div></div>")

            parts.append(
                '<div class="timeline-round-group">'
                '<div class="timeline-round">'
                f"Round {round_number}"
                "</div>"
                '<div class="timeline-row">'
            )

            current_round = round_number
            round_open = True

        else:

            parts.append('<div class="timeline-connector"></div>')

        status_class = event.get(
            "status_class",
            "complete"
        )

        parts.append(
            '<div class="timeline-item">'
            f'<div class="timeline-dot {status_class}"></div>'
            '<div class="timeline-content">'
            f'<div class="timeline-agent">{event["agent"]}</div>'
            f'<div class="timeline-status {status_class}">{event["status"]}</div>'
            "</div>"
            "</div>"
        )

    if round_open:
        parts.append("</div></div>")

    parts.append("</div>")

    html = "".join(parts)

    placeholder.markdown(
        html,
        unsafe_allow_html=True,
    )

# ============================================================
# HEADER
# ============================================================

st.title("V-RAG")

st.markdown(
    '<div class="app-subtitle">'
    "Verified Retrieval-Augmented Generation — every answer is drafted, "
    "cross-examined, and ruled on before it reaches you."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# QUESTION INPUT
# ============================================================

st.markdown(
    '<div class="section-label">Question</div>',
    unsafe_allow_html=True,
)

question = st.text_area(
    "Question",
    placeholder=(
        "Ask a question that requires evidence-based verification..."
    ),
    height=110,
    label_visibility="collapsed",
)

run_button = st.button(
    "Run Verification",
    type="primary",
    use_container_width=True,
)


# ============================================================
# RUN PIPELINE
# ============================================================

if run_button:

    if not question.strip():

        st.warning("Enter a question to run the pipeline.")

    else:

        initial_state = {
            "question": question,
            "retrieved_documents": retrieve(question),
            "responder_output": None,
            "prosecutor_output": None,
            "additional_documents": [],
            "judge_output": None,
            "revision_count": 0,
        }


        # ============================================================
        # LIVE EXECUTION STATUS
        # ============================================================

        st.divider()

        st.markdown(
            '<div class="section-label">Execution</div>',
            unsafe_allow_html=True,
        )

        timeline_placeholder = st.empty()

        execution_events = []

        current_round = 1

        render_timeline(
            execution_events,
            timeline_placeholder,
        )


        final_state = initial_state.copy()


        for update in app.stream(
            initial_state,
            stream_mode="updates",
        ):

            for node_name, node_output in update.items():

                final_state.update(node_output)

                # ====================================================
                # RESPONDER
                # ====================================================

                if node_name == "responder_node":

                    revision_count = node_output.get(
                        "revision_count",
                        final_state.get("revision_count", 0)
                    )

                    current_round = revision_count + 1

                    execution_events.append({
                        "round": current_round,
                        "agent": "Responder",
                        "status": "Complete",
                        "status_class": "complete",
                    })


                # ====================================================
                # PROSECUTOR
                # ====================================================

                elif node_name == "prosecutor_node":

                    execution_events.append({
                        "round": current_round,
                        "agent": "Prosecutor",
                        "status": "Complete",
                        "status_class": "complete",
                    })

                    prosecutor_output = node_output.get(
                        "prosecutor_output"
                    )

                    if (
                        prosecutor_output
                        and prosecutor_output.investigation_request
                    ):

                        execution_events.append({
                            "round": current_round,
                            "agent": "Investigation",
                            "status": "Required",
                            "status_class": "investigation",
                        })


                # ====================================================
                # INVESTIGATION
                # ====================================================

                elif node_name == "investigation_node":

                    additional_docs = node_output.get(
                        "additional_documents",
                        []
                    )

                    if execution_events:

                        execution_events[-1]["status"] = (
                            f"{len(additional_docs)} documents retrieved"
                        )


                # ====================================================
                # JUDGE
                # ====================================================

                elif node_name == "judge_node":

                    judge_output = node_output.get(
                        "judge_output"
                    )

                    if judge_output:

                        if judge_output.decision == "Accept":

                            execution_events.append({
                                "round": current_round,
                                "agent": "Judge",
                                "status": "ACCEPT",
                                "status_class": "accept",
                            })

                        else:

                            execution_events.append({
                                "round": current_round,
                                "agent": "Judge",
                                "status": "REVISION REQUIRED",
                                "status_class": "revise",
                            })


                # ====================================================
                # UPDATE TIMELINE
                # ====================================================

                render_timeline(
                    execution_events,
                    timeline_placeholder,
                )


        result = final_state


        # ====================================================
        # EXTRACT FINAL STATE
        # ====================================================

        responder_output = result["responder_output"]
        prosecutor_output = result["prosecutor_output"]
        judge_output = result["judge_output"]
        additional_documents = result["additional_documents"]
        revision_count = result["revision_count"]


        # ====================================================
        # FINAL ANSWER
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="final-answer-label">Final Answer</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="final-answer-box">
                {responder_output.answer}
            </div>
            """,
            unsafe_allow_html=True,
        )


        # ====================================================
        # RESPONDER + PROSECUTOR
        # ====================================================

        st.divider()

        responder_col, prosecutor_col = st.columns(
            2,
            gap="large",
        )


        # ====================================================
        # RESPONDER
        # ====================================================

        with responder_col:

            st.markdown(
                """
                <div class="agent-block">
                <div class="agent-eyebrow responder-eyebrow">01 · BUILDS THE CASE</div>
                <div class="agent-header responder-header">RESPONDER</div>
                <div class="agent-description">
                    Drafts the answer and ties every claim it makes back to
                    a specific piece of evidence.
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("**Claims**")

            for i, claim in enumerate(
                responder_output.claims,
                start=1,
            ):

                with st.expander(
                    f"Claim {i}",
                    expanded=False,
                ):

                    st.write(
                        claim.claim_text
                    )

                    st.markdown(
                        "**Evidence References**"
                    )

                    if claim.evidence_references:

                        for evidence in (
                            claim.evidence_references
                        ):

                            st.markdown(
                                f"""
                                <div class="evidence-reference">
                                    <div class="evidence-source">
                                        {evidence.source}
                                    </div>
                                    <div class="evidence-chunk">
                                        Chunk {evidence.chunk_id}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    else:

                        st.caption(
                            "No evidence reference provided."
                        )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


        # ====================================================
        # PROSECUTOR
        # ====================================================

        with prosecutor_col:

            st.markdown(
                """
                <div class="agent-block">
                <div class="agent-eyebrow prosecutor-eyebrow">02 · TESTS THE CASE</div>
                <div class="agent-header prosecutor-header">PROSECUTOR</div>
                <div class="agent-description">
                    Challenges each claim, flags what's unsupported, and
                    requests further evidence where the case is thin.
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                "**Risk Assessments**"
            )

            for i, assessment in enumerate(
                prosecutor_output.risk_assessments,
                start=1,
            ):

                risk = assessment.risk.lower()

                risk_class = (
                    f"risk-{risk}"
                    if risk in ["low", "medium", "high"]
                    else "risk-medium"
                )

                with st.expander(
                    f"Claim {i}",
                    expanded=False,
                ):

                    st.markdown(
                        f"""
                        <span class="risk-label {risk_class}">
                            {assessment.risk}
                        </span>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.write(
                        assessment.claim_text
                    )

                    st.markdown(
                        "**Reason**"
                    )

                    st.write(
                        assessment.reason
                    )


            # ------------------------------------------------
            # INVESTIGATION
            # ------------------------------------------------

            st.markdown(
                "**Investigation**"
            )

            investigation = (
                prosecutor_output.investigation_request
            )

            if investigation:

                st.warning(
                    "Additional investigation requested."
                )

                st.markdown(
                    "**Search Query**"
                )

                st.code(
                    investigation.search_query
                )

                st.markdown(
                    "**Claims Investigated**"
                )

                for claim in (
                    investigation.claim_texts
                ):

                    st.write(
                        f"• {claim}"
                    )

            else:

                st.success(
                    "No additional investigation required."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


        # ====================================================
        # JUDGE
        # ====================================================

        st.divider()

        st.markdown(
            """
            <div class="agent-eyebrow judge-eyebrow">03 · RULES ON THE CASE</div>
            <div class="agent-header judge-header">JUDGE</div>
            <div class="agent-description" style="border-bottom: none; margin-bottom: 1.6rem;">
                Weighs the responder's answer against the prosecutor's
                challenges and the available evidence to reach a final ruling.
            </div>
            """,
            unsafe_allow_html=True,
        )

        judge_left, judge_right = st.columns(
            [1, 3],
            gap="large",
        )


        # ----------------------------------------------------
        # DECISION
        # ----------------------------------------------------

        with judge_left:

            decision = judge_output.decision

            seal_class = (
                "verdict-accept"
                if decision == "Accept"
                else "verdict-revise"
            )

            st.markdown(
                f"""
                <div class="verdict-seal {seal_class}">
                    <div class="verdict-seal-label">Ruling</div>
                    <div class="verdict-seal-value">{decision.upper()}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")

            st.metric(
                "Revision Count",
                revision_count,
            )


        # ----------------------------------------------------
        # REASONING
        # ----------------------------------------------------

        with judge_right:

            st.markdown(
                "**Reasoning**"
            )

            st.write(
                judge_output.reasoning
            )

            if judge_output.revision_instructions:

                st.markdown(
                    "**Revision Instructions**"
                )

                st.info(
                    judge_output.revision_instructions
                )


        # ====================================================
        # PIPELINE DETAILS
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="pipeline-heading">Pipeline Details</div>',
            unsafe_allow_html=True,
        )

        investigation_performed = (
            len(additional_documents) > 0
        )

        col1, col2, col3, col4 = st.columns(
            4,
            gap="medium",
        )

        with col1:

            st.metric(
                "Revisions",
                revision_count,
            )

        with col2:

            st.metric(
                "Investigation",
                "Yes"
                if investigation_performed
                else "No",
            )

        with col3:

            st.metric(
                "Additional Documents",
                len(additional_documents),
            )

        with col4:

            st.metric(
                "Final Decision",
                judge_output.decision.upper(),
            )


        # ====================================================
        # ADDITIONAL DOCUMENTS
        # ====================================================

        if additional_documents:

            st.divider()

            with st.expander(
                "View Investigation Documents"
            ):

                for i, doc in enumerate(
                    additional_documents,
                    start=1,
                ):

                    source = doc.metadata.get(
                        "source",
                        "Unknown",
                    )

                    chunk_id = doc.metadata.get(
                        "chunk_id",
                        "Unknown",
                    )

                    st.markdown(
                        f"**Document {i}**"
                    )

                    st.caption(
                        f"{source} · Chunk {chunk_id}"
                    )

                    st.write(
                        doc.page_content
                    )

                    if i < len(additional_documents):

                        st.divider()
