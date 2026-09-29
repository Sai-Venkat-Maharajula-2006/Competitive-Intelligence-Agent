import nest_asyncio
nest_asyncio.apply()

import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from groq import Groq, APIError, APIConnectionError, RateLimitError
from hindsight_client import Hindsight

# ── Config ──────────────────────────────────────────────────────────────────
load_dotenv()

GROQ_API_KEY       = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY  = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
MEMORY_BANK        = "nexuscorp-intelligence-bank"
GROQ_MODEL         = "openai/gpt-oss-120b"

# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexusCorp Executive Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Custom CSS ────────────────────────────────────────────────────────
def load_custom_css():
    css_file = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()

# ── Clients ──────────────────────────────────────────────────────────────────
@st.cache_resource
def get_clients():
    groq_client      = Groq(api_key=GROQ_API_KEY)
    hindsight_client = Hindsight(base_url=HINDSIGHT_BASE_URL, api_key=HINDSIGHT_API_KEY)
    return groq_client, hindsight_client

groq_client, hindsight_client = get_clients()

# ── Header Banner ────────────────────────────────────────────────────────────
st.markdown("""
<div class="exec-header">
    <div>
        <h1 class="exec-header-title">NexusCorp Strategic Intelligence</h1>
        <p class="exec-header-subtitle">Executive Command Center · Hindsight Persistent Memory · Groq Accelerated Analysis</p>
    </div>
    <div>
        <span class="badge-live"><span class="pulse-dot"></span> Live Intelligence</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Executive Metrics Row ────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Primary Competitor</div>
        <div class="metric-value">Synthetix Corp</div>
        <div class="metric-subtext">Leader (Gartner MQ) · GovPods Push</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Monitored Rivals</div>
        <div class="metric-value">3 Entities</div>
        <div class="metric-subtext">Synthetix, OrbitEdge, DataVault</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Pipeline at Risk</div>
        <div class="metric-value">$13.4M ARR</div>
        <div class="metric-subtext">UK CDDO Framework ($12M) + Logistics</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Memory Bank Depth</div>
        <div class="metric-value">10 Verified Events</div>
        <div class="metric-subtext">March 2026 – Sept 2026 Chronology</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# ── Sidebar: Form-based Intel Ingestion ──────────────────────────────────────
with st.sidebar:
    st.markdown("### 📥 Ingest Competitor Intel")
    st.caption("Capture breaking competitor maneuvers directly into the persistent intelligence memory bank.")

    with st.form("competitor_update_form", clear_on_submit=True):
        update_text = st.text_area(
            "Intelligence Brief",
            placeholder=(
                "e.g. Synthetix Corp announced aggressive 25% discounting on enterprise "
                "multi-year commitments to lock out competitors in EMEA..."
            ),
            height=180,
            label_visibility="collapsed",
        )
        
        submitted = st.form_submit_button("⚡ Save to Memory Bank", use_container_width=True, type="primary")

        if submitted:
            if not update_text.strip():
                st.warning("⚠️ Please provide an intelligence update before saving.")
            else:
                with st.spinner("Retaining update in memory bank..."):
                    try:
                        # Clean execution via nest_asyncio & asyncio.run without destroying persistent loop
                        retain_fn = getattr(hindsight_client, "aretain", hindsight_client.retain)
                        asyncio.run(
                            retain_fn(
                                bank_id=MEMORY_BANK,
                                content=update_text.strip(),
                            )
                        )
                        st.toast("Intelligence successfully stored into memory bank!", icon="✅")
                    except Exception as e:
                        st.error(f"❌ Failed to retain update: {e}")

    st.markdown("---")
    st.markdown("#### ⚙️ System Configuration")
    use_memory = st.toggle("🧠 Enable Hindsight Memory Bank", value=True)
    st.markdown(f"**Bank ID:** `{MEMORY_BANK}`")
    st.markdown(f"**Engine:** `{GROQ_MODEL}`")
    st.markdown(f"**Recall Endpoint:** `hindsight.vectorize.io`")

# ── Main View: Strategic Briefing & Chat ─────────────────────────────────────
st.subheader("🔭 Strategic Query & Threat Synthesis")
st.caption("Pose strategic questions to cross-reference historical competitor signals with real-time reasoning.")

# Chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous conversation
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Interactive chat input
user_query = st.chat_input("Ask a strategic question (e.g. 'What is Synthetix Corp's GovPods strategy and how does it hurt us?')...")

# ── Interactive Chat Input Processing ────────────────────────────────────────
if user_query:
    # Add and render user query
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Synthesizing strategic brief..."):

            # ── Step 1: Recall context using Hindsight (If toggle is ON) ────
            recalled_context = ""
            raw_recall_preview = ""

            if use_memory:
                try:
                    # Check for synchronous recall first to avoid asyncio task/timeout issues in Streamlit
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                    recall_response = loop.run_until_complete(
                        hindsight_client.arecall(
                            bank_id=MEMORY_BANK,
                            query=user_query,
                            max_tokens=4096,
                            budget="mid"
                        )
                    )

                    recalled_context = str(recall_response) if recall_response else "No exact historical match found."
                    raw_recall_preview = recalled_context[:1200] + ("\n... [truncated]" if len(recalled_context) > 1200 else "")
                except Exception as e:
                    st.warning(f"⚠️ Memory recall notice: {e}. Generating response without historical context.")
                    recalled_context = "Memory recall error encountered."
            else:
                recalled_context = "⚠️ HINDSIGHT MEMORY BANK IS CURRENTLY DISABLED (STATELESS MODE)."

            # ── Step 2: Formulate Groq prompt ────────────────────────────
            if use_memory:
                system_prompt = (
                    "You are the Chief Competitive Intelligence Officer for NexusCorp. "
                    "Synthesize competitor actions into concise, high-impact executive briefings. "
                    "Ground your analysis in the recalled memory context below when available. "
                    "Organize your briefing strictly with: \n"
                    "### 1. Situation Analysis\n"
                    "### 2. Strategic Threat Assessment\n"
                    "### 3. Immediate Recommended Actions\n\n"
                    f"=== VERIFIED HISTORICAL INTEL (HINDSIGHT) ===\n{recalled_context}\n"
                    "============================================="
                )
            else:
                system_prompt = (
                    "You are the Chief Competitive Intelligence Officer for NexusCorp. "
                    "Answer the user's question purely statelessly without using any persistent historical context or memory bank. "
                    "Organize your briefing strictly with: \n"
                    "### 1. Situation Analysis\n"
                    "### 2. Strategic Threat Assessment\n"
                    "### 3. Immediate Recommended Actions"
                )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_query},
            ]

            # ── Step 3: Groq LLM Inference with Error Handling ───────────
            analysis = ""
            try:
                groq_resp = groq_client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=messages,
                    temperature=0.35,
                    max_tokens=1024,
                )
                analysis = groq_resp.choices[0].message.content

            except RateLimitError as e:
                analysis = f"⚠️ **Rate Limit Alert:** Groq API rate threshold met. Please retry in a few moments.\n\n_{e}_"
            except APIConnectionError as e:
                analysis = f"❌ **Network Error:** Unable to reach Groq API. Check connectivity and credentials.\n\n_{e}_"
            except APIError as e:
                analysis = f"❌ **API Error (Status {e.status_code}):** {e}"
            except Exception as e:
                analysis = f"❌ **System Exception:** {e}"

            # ── Step 4: Render Assistant Briefing ─────────────────────────
            st.markdown(analysis)

            # Clean expander to inspect raw recall data without cluttering UI
            if use_memory and raw_recall_preview:
                with st.expander("🔍 View Raw Recall Context & Evidence Citations", expanded=False):
                    st.code(raw_recall_preview, language="text")

    st.session_state.chat_history.append({"role": "assistant", "content": analysis})