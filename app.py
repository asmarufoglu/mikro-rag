import streamlit as st
import pandas as pd
from utils.retrieval import build_index, search_logs
import os
from dotenv import load_dotenv
import google.generativeai as genai
from llm import generate_answer


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI-Powered Network Log Assistant",
    page_icon="📡",
    layout="wide"
)

# ---------- CUSTOM TOOLTIP STYLE ----------
st.markdown("""
    <style>
    /* Tooltip container */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    /* Tooltip text */
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 260px;
        background-color: #0f243e; 
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 8px;
        position: fixed;  
        z-index: 9999;  
        bottom: auto;
        left: auto;
        margin-left: 10px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.3);
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("📡 AI-Powered Network Log Assistant")
st.caption("An AI-driven automation demo for real-time network log analysis and monitoring.")
st.divider()

# ---------- SIDEBAR ----------
st.sidebar.header("⚙️ System Overview")
with st.sidebar.expander("ℹ️ What does this do?", expanded=True):
    st.markdown("""
    This app demonstrates **AI-powered network automation** via a Retrieval-Augmented Generation (RAG) workflow:
    - Semantic indexing and search of network logs  
    - Auto-updating FAISS embeddings on data change  
    - Evaluating retrieval performance via precision@k  
    """)

# ---------- LOAD INDEX ----------
if "index" not in st.session_state:
    with st.spinner("Building FAISS index..."):
        index, df = build_index()
        st.session_state["index"] = index
        st.session_state["df"] = df

# ---------- FAISS INDEX STATUS ----------
with st.sidebar.container():
    st.markdown("""
    <div class="tooltip">
        ✅ <b>FAISS Index Ready</b>
        <span class="tooltiptext">
            The FAISS index continuously monitors and stores dense embeddings of log messages.<br>
            It enables semantic similarity search when new network data is added — effectively
            acting as the AI memory of the system.
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Vector store for semantic retrieval of network logs.")

# ---------- LLM CONFIG ----------
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDCz7OKVDx_J5VK1FZcOuXBf_SF4xiC3Wo"))


# ---------- EVALUATION METRICS ----------
st.sidebar.markdown("---")
st.sidebar.header("📊 Evaluation Metrics")
try:
    eval_df = pd.read_csv("data/eval_results.csv")
    st.sidebar.dataframe(eval_df, hide_index=True, width="stretch")

    st.sidebar.markdown("""
    <div class="tooltip" style="margin-top:8px;">
        🧠 <b>Metric Info</b>
        <span class="tooltiptext" style="top: 220px; left: 220px;">
            <b>Precision@k</b>: Measures how many of the top-k retrieved logs are relevant.<br><br>
            <b>Latency (s)</b>: Average response time per query.<br><br>
            Higher precision = better accuracy.<br>
            Lower latency = faster retrieval.
        </span>
    </div>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.sidebar.info("Run `evaluate.py` to generate metrics.")

# ---------- QUERY AREA ----------
st.markdown("""
### 🔍 <div class="tooltip">Query the Log Index
<span class="tooltiptext">
This module performs semantic search over indexed logs.<br>
When you enter a natural language query, it encodes your text into a vector and retrieves
the most contextually similar network events.
</span>
</div>
""", unsafe_allow_html=True)

query = st.text_input("Enter your query (e.g., 'packet loss in node 1'):")

if query:
    with st.spinner("Retrieving logs..."):
        results, scores = search_logs(query, st.session_state["index"], st.session_state["df"])
        df_display = results.copy()
        df_display["similarity"] = [round(s, 2) for s in scores]

        st.markdown("""
        ### 📑 Retrieved Logs
        <div class="tooltip">
        <span class="tooltiptext">
        Each row corresponds to a log message retrieved based on semantic similarity.<br>
        <b>Higher similarity → stronger contextual relevance.</b>
        </span>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            df_display[["timestamp", "node_id", "severity", "alarm_code", "message", "similarity"]],
            hide_index=True,
            width="content"
        )

        # ---------- SUMMARY ----------
        context_text = " | ".join(results["message"].tolist())

        st.markdown("""
        ### 🧠 Root-Cause Summary
        <div class="tooltip">
        <span class="tooltiptext">
        This summary is generated by Gemini 2.5 Flash.  
        It interprets the retrieved network logs and infers the most likely root cause.
        </span>
        </div>
        """, unsafe_allow_html=True)

        answer = generate_answer(context_text=context_text, user_input=query)

        if answer.startswith("⚠️"):
            st.warning(answer)
        else:
            st.success(answer)



# ---------- ABOUT ----------
st.sidebar.markdown("---")
st.sidebar.header("👨‍💻 About this Project")
st.sidebar.markdown("""
**Semih Marufoğlu**  
https://github.com/asmarufoglu
""")
