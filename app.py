import os
from dotenv import load_dotenv
import validators
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Distill — AI Summarizer",
    page_icon="▲",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #080B12 !important;
    color: #E8EAF0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(56, 112, 255, 0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 85% 80%, rgba(139, 92, 246, 0.10) 0%, transparent 55%),
        #080B12 !important;
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container {
    max-width: 760px !important;
    padding: 3.5rem 2rem 5rem !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }

/* ── Typography ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
}

/* ── Hero section ── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 0 3rem;
}
.hero-badge {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7B9CFF;
    background: rgba(56, 112, 255, 0.10);
    border: 1px solid rgba(56, 112, 255, 0.22);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    margin-bottom: 1.6rem;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.6rem, 6vw, 4rem) !important;
    font-weight: 800 !important;
    line-height: 1.08 !important;
    letter-spacing: -0.03em !important;
    color: #FFFFFF !important;
    margin-bottom: 1.1rem !important;
}
.hero-title span {
    background: linear-gradient(95deg, #4F8CFF 0%, #A78BFA 55%, #60C8FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 300;
    color: #8892AA;
    line-height: 1.65;
    max-width: 480px;
    margin: 0 auto;
}

/* ── Divider ── */
.g-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,112,255,0.25) 40%, rgba(139,92,246,0.20) 60%, transparent);
    margin: 2rem 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.032);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 2rem 2rem 1.6rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.4rem;
}
.input-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #5A6680;
    margin-bottom: 0.7rem;
}

/* ── Streamlit input override ── */
[data-testid="stTextInput"] input {
    background: rgba(10, 14, 26, 0.7) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    color: #E8EAF0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.97rem !important;
    padding: 0.75rem 1.1rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(79, 140, 255, 0.50) !important;
    box-shadow: 0 0 0 3px rgba(79, 140, 255, 0.10) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #3D4760 !important; }
[data-testid="stTextInput"] label { display: none !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #3B6FE8 0%, #7C5CDE 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 0.75rem 1.5rem !important;
    cursor: pointer !important;
    transition: opacity 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease !important;
    box-shadow: 0 4px 24px rgba(59, 111, 232, 0.28) !important;
    margin-top: 0.5rem !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(59, 111, 232, 0.38) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0px) !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: #4F8CFF !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}

/* ── Alert / error ── */
[data-testid="stAlert"] {
    background: rgba(239, 68, 68, 0.08) !important;
    border: 1px solid rgba(239, 68, 68, 0.22) !important;
    border-radius: 10px !important;
    color: #FCA5A5 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Success ── */
.stSuccess {
    background: rgba(16, 185, 129, 0.08) !important;
    border: 1px solid rgba(16, 185, 129, 0.22) !important;
    border-radius: 10px !important;
    color: #6EE7B7 !important;
}

/* ── Summary output ── */
.summary-wrap {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 2rem 2rem 1.6rem;
    margin-top: 1.8rem;
    position: relative;
    overflow: hidden;
}
.summary-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #4F8CFF, #A78BFA, #60C8FF);
}
.summary-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.4rem;
}
.summary-tag {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #4F8CFF;
    background: rgba(79, 140, 255, 0.10);
    border: 1px solid rgba(79, 140, 255, 0.20);
    border-radius: 100px;
    padding: 0.28rem 0.75rem;
}
.summary-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.97rem;
    font-weight: 300;
    line-height: 1.8;
    color: #C8D0E0;
    white-space: pre-wrap;
}

/* ── Download button override ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,0.04) !important;
    color: #8892AA !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.04em !important;
    padding: 0.5rem 1.1rem !important;
    margin-top: 1.4rem !important;
    box-shadow: none !important;
    transition: background 0.18s, color 0.18s, border-color 0.18s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(79, 140, 255, 0.10) !important;
    color: #7B9CFF !important;
    border-color: rgba(79, 140, 255, 0.30) !important;
    transform: none !important;
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}
.stat-pill {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    color: #4A5568;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 6px;
    padding: 0.28rem 0.7rem;
}
.stat-pill b { color: #6B7FA3; font-weight: 500; }

/* ── Footer ── */
.footer-text {
    text-align: center;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    color: #2A3245;
    padding-top: 3rem;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)

# ── Setup ──────────────────────────────────────────────────────────────────────
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.3-70b-versatile",
    temperature=0,
)

prompt_template = """You are an advanced AI summarizer.

Analyze the following text and provide a concise summary that captures the main points and key information. Ensure that the summary is clear, coherent, and retains the essential meaning of the original content.

Requirements:
- Generate a comprehensive summary
- Cover all important topics and details
- Use Heading and Bullet points for better readability
- Include examples if present in the original text
- Keep Technical details intact if they are crucial to understanding the content
- Make the summary educational and informative, suitable for readers who want to grasp the core ideas without reading the entire text.
- Summary length should be around 500 - 600 words, but can be adjusted based on the length and complexity of the original text.

Content to summarize: {text}
"""

prompt = PromptTemplate(input_variables=["text"], template=prompt_template)

refine_prompt_template = PromptTemplate(
    input_variables=["text"],
    template="""Combine the following partial summaries into a detailed, structured and comprehensive final summary.

{text}

Final summary should be educational and informative, suitable for readers who want to grasp the core ideas without reading the entire text. Use Heading and Bullet points for better readability."""
)


def summarize_url(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        loader = YoutubeLoader.from_youtube_url(url)
    else:
        loader = UnstructuredURLLoader(
            urls=[url],
            ssl_verify=False,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        )
    documents = loader.load()
    content = "\n".join([doc.page_content for doc in documents])

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=500, length_function=len
    )
    splitted_docs = text_splitter.create_documents([content])

    chain = prompt | llm | StrOutputParser()
    final_summary = ""
    for doc in splitted_docs:
        final_summary += chain.invoke({"text": doc.page_content}) + "\n\n"

    refine_chain = refine_prompt_template | llm | StrOutputParser()
    summary = refine_chain.invoke({"text": final_summary})
    return summary


# ── UI ─────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">Powered by Groq + LangChain</div>
    <h1 class="hero-title">Extract what<br><span>actually matters</span></h1>
    <p class="hero-sub">Paste any webpage , blog , article or research paper URL. Get a precise, structured summary in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="g-divider"></div>', unsafe_allow_html=True)

# Input card
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Source URL</div>', unsafe_allow_html=True)
url = st.text_input("url", placeholder="https://youtube.com/watch?v=...  or any webpage", label_visibility="collapsed")
summarize_btn = st.button("Generate Summary")
st.markdown('</div>', unsafe_allow_html=True)

# ── Logic ──────────────────────────────────────────────────────────────────────
if summarize_btn:
    if not groq_api_key:
        st.error("GROQ_API_KEY not found. Check your .env file.")
    elif not url or not url.strip():
        st.error("Please enter a URL before proceeding.")
    elif not validators.url(url):
        st.error("The URL entered does not appear to be valid. Please double-check.")
    else:
        try:
            with st.spinner("Analyzing and summarizing content..."):
                summary = summarize_url(url)

            word_count = len(summary.split())
            char_count = len(summary)
            source_type = "YouTube" if ("youtube.com" in url or "youtu.be" in url) else "Webpage"

            st.markdown(f"""
            <div class="summary-wrap">
                <div class="summary-header">
                    <span class="summary-tag">Summary</span>
                </div>
                <div class="summary-body">{summary}</div>
                <div class="stats-row">
                    <span class="stat-pill"><b>{word_count}</b> words</span>
                    <span class="stat-pill"><b>{char_count}</b> characters</span>
                    <span class="stat-pill"><b>{source_type}</b> source</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="Download as .txt",
                data=summary,
                file_name="summary.txt",
                mime="text/plain",
            )

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.markdown('<div class="footer-text">Distill — AI Summarization Engine</div>', unsafe_allow_html=True)
