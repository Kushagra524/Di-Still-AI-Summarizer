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

# Page config 
st.set_page_config(
    page_title="Distill — AI Summarizer",
    page_icon="▲",
    layout="centered",
    initial_sidebar_state="collapsed",
)



# Global CSS 
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
        radial-gradient(ellipse 90% 55% at 50% -5%, rgba(56, 112, 255, 0.22) 0%, transparent 60%),
        radial-gradient(ellipse 70% 45% at 85% 80%, rgba(139, 92, 246, 0.14) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 10% 70%, rgba(96, 200, 255, 0.08) 0%, transparent 50%),
        #080B12 !important;
    min-height: 100vh;
}

/* Animated background orbs */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -20%;
    left: -10%;
    width: 55%;
    height: 55%;
    background: radial-gradient(ellipse, rgba(56, 112, 255, 0.07) 0%, transparent 70%);
    border-radius: 50%;
    animation: orbFloat1 12s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    bottom: -10%;
    right: -5%;
    width: 45%;
    height: 45%;
    background: radial-gradient(ellipse, rgba(139, 92, 246, 0.07) 0%, transparent 70%);
    border-radius: 50%;
    animation: orbFloat2 15s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes orbFloat1 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(3%, 5%) scale(1.05); }
    66% { transform: translate(-2%, 3%) scale(0.97); }
}
@keyframes orbFloat2 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    40% { transform: translate(-4%, -3%) scale(1.08); }
    70% { transform: translate(2%, -5%) scale(0.95); }
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container {
    max-width: 760px !important;
    padding: 3.5rem 2rem 5rem !important;
    position: relative;
    z-index: 1;
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
    animation: heroFadeUp 0.8s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes heroFadeUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7B9CFF;
    background: rgba(56, 112, 255, 0.10);
    border: 1px solid rgba(56, 112, 255, 0.28);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 0 16px rgba(56, 112, 255, 0.12), inset 0 1px 0 rgba(255,255,255,0.06);
    position: relative;
    overflow: hidden;
}

.hero-badge::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(from 0deg, transparent 0deg, rgba(79,140,255,0.08) 60deg, transparent 120deg);
    animation: badgeSpin 4s linear infinite;
}

@keyframes badgeSpin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}

.hero-badge::after {
    content: '●';
    font-size: 0.4rem;
    color: #4F8CFF;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.6rem, 6vw, 4rem) !important;
    font-weight: 800 !important;
    line-height: 1.08 !important;
    letter-spacing: -0.03em !important;
    color: #FFFFFF !important;
    margin-bottom: 1.1rem !important;
    animation: heroFadeUp 0.8s 0.1s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.hero-title span {
    background: linear-gradient(95deg, #4F8CFF 0%, #A78BFA 55%, #60C8FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 28px rgba(79,140,255,0.35));
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 300;
    color: #8892AA;
    line-height: 1.65;
    max-width: 480px;
    margin: 0 auto;
    text-align: center;
    animation: heroFadeUp 0.8s 0.2s cubic-bezier(0.22, 1, 0.36, 1) both;
}

/* ── Divider ── */
.g-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,112,255,0.30) 35%, rgba(167,139,250,0.25) 65%, transparent);
    margin: 2rem 0;
    position: relative;
}

.g-divider::after {
    content: '';
    position: absolute;
    top: 0; left: 30%; right: 30%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    filter: blur(1px);
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
    background: rgba(10, 14, 26, 0.75) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    color: #E8EAF0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.97rem !important;
    padding: 0.75rem 1.1rem !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease !important;
}
[data-testid="stTextInput"] input:focus {
    background: rgba(10, 14, 26, 0.9) !important;
    border-color: rgba(79, 140, 255, 0.55) !important;
    box-shadow: 0 0 0 3px rgba(79, 140, 255, 0.12), 0 0 20px rgba(79,140,255,0.08) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #3D4760 !important; }
[data-testid="stTextInput"] label { display: none !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #2D5BE3 0%, #6B4FD8 50%, #9B59F5 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 1.5rem !important;
    cursor: pointer !important;
    transition: all 0.22s cubic-bezier(0.22, 1, 0.36, 1) !important;
    box-shadow:
        0 4px 24px rgba(59, 111, 232, 0.35),
        0 1px 0 rgba(255,255,255,0.12) inset,
        0 -1px 0 rgba(0,0,0,0.2) inset !important;
    margin-top: 0.6rem !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="stButton"] > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important; left: -100% !important;
    width: 100% !important; height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.10), transparent) !important;
    transition: left 0.45s ease !important;
}

[data-testid="stButton"] > button:hover::before {
    left: 100% !important;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #3B6FE8 0%, #7C5CDE 50%, #A978FF 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow:
        0 10px 36px rgba(79, 111, 232, 0.45),
        0 4px 16px rgba(139,92,246,0.25),
        0 1px 0 rgba(255,255,255,0.15) inset !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0px) scale(0.99) !important;
    box-shadow: 0 2px 12px rgba(59, 111, 232, 0.25) !important;
}

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
    background: rgba(255,255,255,0.022);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 2rem 2rem 1.6rem;
    margin-top: 1.8rem;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(16px);
    animation: summaryReveal 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes summaryReveal {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Top gradient border */
.summary-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #4F8CFF 0%, #A78BFA 50%, #60C8FF 100%);
    box-shadow: 0 0 16px rgba(79,140,255,0.5);
}

/* Glow in bottom-right corner */
.summary-wrap::after {
    content: '';
    position: absolute;
    bottom: -30%;
    right: -10%;
    width: 50%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(139,92,246,0.06) 0%, transparent 70%);
    pointer-events: none;
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
    border: 1px solid rgba(79, 140, 255, 0.22);
    border-radius: 100px;
    padding: 0.28rem 0.75rem;
    box-shadow: 0 0 12px rgba(79,140,255,0.12);
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
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.04em !important;
    padding: 0.5rem 1.1rem !important;
    margin-top: 1.4rem !important;
    box-shadow: none !important;
    transition: background 0.2s, color 0.2s, border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(79, 140, 255, 0.10) !important;
    color: #7B9CFF !important;
    border-color: rgba(79, 140, 255, 0.35) !important;
    box-shadow: 0 0 16px rgba(79,140,255,0.12) !important;
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
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 6px;
    padding: 0.28rem 0.7rem;
    transition: border-color 0.2s, color 0.2s;
}
.stat-pill:hover {
    border-color: rgba(79,140,255,0.20);
    color: #6B7FA3;
}
.stat-pill b { color: #6B7FA3; font-weight: 500; }

/* ── Footer ── */
.footer-text {
    text-align: center;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    color: #2A3245;
    padding-top: 3rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)

# Setup 
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=groq_api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct",
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


import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

def load_url(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers, timeout=15, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    
    text = soup.get_text(separator="\n", strip=True)
    return [Document(page_content=text)]


def prepare_final_input(url: str) -> tuple:
    """Loads content, chunks it, and returns (final_input_text, is_single_chunk, source_type).
    For single chunk: returns raw chunk text.
    For multi chunk: runs all intermediate summarizations and returns combined text for final refine.
    """
    if "youtube.com" in url or "youtu.be" in url:
        loader = YoutubeLoader.from_youtube_url(url)
        documents = loader.load()
        source_type = "YouTube"
    else:
        documents = load_url(url)
        source_type = "Webpage"

    content = "\n".join([doc.page_content for doc in documents])

    if not content.strip():
        raise ValueError("Could not extract any content from this URL. The page may be empty or blocked.")

    MAX_CONTENT_LENGTH = 50000
    if len(content) > MAX_CONTENT_LENGTH:
        content = content[:MAX_CONTENT_LENGTH]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000, chunk_overlap=200, length_function=len
    )
    splitted_docs = text_splitter.create_documents([content])

    chain = prompt | llm | StrOutputParser()

    # Single chunk — stream it directly
    if len(splitted_docs) == 1:
        return splitted_docs[0].page_content, True, source_type, chain

    # Multi-chunk — process all intermediate chunks normally, prepare final input
    partial_summaries = []
    for doc in splitted_docs:
        summary_chunk = chain.invoke({"text": doc.page_content})
        partial_summaries.append(summary_chunk)

    refine_chain = refine_prompt_template | llm | StrOutputParser()
    BATCH_SIZE = 5

    while len(partial_summaries) > 1:
        new_summaries = []
        for i in range(0, len(partial_summaries), BATCH_SIZE):
            batch = partial_summaries[i:i + BATCH_SIZE]
            combined_text = "\n\n".join(batch)
            if len(batch) == 1:
                new_summaries.append(batch[0])
            else:
                # Keep streaming only for the very last refine call
                if len(partial_summaries) <= BATCH_SIZE:
                    return combined_text, False, source_type, refine_chain
                refined = refine_chain.invoke({"text": combined_text})
                new_summaries.append(refined)
        partial_summaries = new_summaries

    # Fallback: only one summary left, stream it as a single-chunk
    return partial_summaries[0], None, source_type, None  # already done, no streaming needed


# UI
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">Powered by Groq + LangChain</div>
    <h1 class="hero-title">Extract what<br><span>actually matters</span></h1>
    <p class="hero-sub">Paste any webpage , article , blog or research paperr. Get a precise, structured summary in seconds.</p>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="g-divider"></div>', unsafe_allow_html=True)

# Input card
# st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Source URL</div>', unsafe_allow_html=True)
url = st.text_input("url", placeholder="https://youtube.com/watch?v=...  or any webpage", label_visibility="collapsed")
summarize_btn = st.button("⚡ Generate Summary")
# st.markdown('</div>', unsafe_allow_html=True)

# Logic 
if summarize_btn:
    if not groq_api_key:
        st.error("GROQ_API_KEY not found. Check your .env file.")
    elif not url or not url.strip():
        st.error("Please enter a URL before proceeding.")
    elif not validators.url(url):
        st.error("The URL entered does not appear to be valid. Please double-check.")
    else:
        try:
            # Step 1: Load & prepare (show spinner during heavy lifting)
            with st.spinner("Loading and processing content..."):
                final_input, is_single_chunk, source_type, final_chain = prepare_final_input(url)

            # Step 2: Stream or display the final summary
            summary = ""

            # Case: already fully resolved (edge case fallback)
            if is_single_chunk is None:
                summary = final_input
                word_count = len(summary.split())
                char_count = len(summary)
                st.markdown(f"""
                <div class="summary-wrap">
                    <div class="summary-header"><span class="summary-tag">Summary</span></div>
                    <div class="summary-body">{summary}</div>
                    <div class="stats-row">
                        <span class="stat-pill"><b>{word_count}</b> words</span>
                        <span class="stat-pill"><b>{char_count}</b> characters</span>
                        <span class="stat-pill"><b>{source_type}</b> source</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                # Streaming: show the card shell immediately, stream text inside
                st.markdown("""
                <div class="summary-wrap" id="summary-card">
                    <div class="summary-header"><span class="summary-tag">Summary</span></div>
                </div>
                """, unsafe_allow_html=True)

                stream_placeholder = st.empty()

                input_key = "text"
                stream = final_chain.stream({input_key: final_input})

                for chunk in stream:
                    summary += chunk
                    stream_placeholder.markdown(
                        f"""<div class="summary-body" style="
                            font-family:'DM Sans',sans-serif;
                            font-size:0.97rem;
                            font-weight:300;
                            line-height:1.8;
                            color:#C8D0E0;
                            white-space:pre-wrap;
                            margin-top: -0.5rem;
                        ">{summary}▌</div>""",
                        unsafe_allow_html=True
                    )

                # Final render without cursor
                word_count = len(summary.split())
                char_count = len(summary)
                stream_placeholder.markdown(
                    f"""<div class="summary-body" style="
                        font-family:'DM Sans',sans-serif;
                        font-size:0.97rem;
                        font-weight:300;
                        line-height:1.8;
                        color:#C8D0E0;
                        white-space:pre-wrap;
                        margin-top: -0.5rem;
                    ">{summary}</div>
                    <div class="stats-row" style="display:flex;gap:1rem;margin-top:1rem;">
                        <span class="stat-pill" style="font-family:'DM Sans',sans-serif;font-size:0.72rem;color:#6B7FA3;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:6px;padding:0.28rem 0.7rem;"><b>{word_count}</b> words</span>
                        <span class="stat-pill" style="font-family:'DM Sans',sans-serif;font-size:0.72rem;color:#6B7FA3;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:6px;padding:0.28rem 0.7rem;"><b>{char_count}</b> characters</span>
                        <span class="stat-pill" style="font-family:'DM Sans',sans-serif;font-size:0.72rem;color:#6B7FA3;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:6px;padding:0.28rem 0.7rem;"><b>{source_type}</b> source</span>
                    </div>""",
                    unsafe_allow_html=True
                )

            st.download_button(
                label="↓ Download as .txt",
                data=summary,
                file_name="summary.txt",
                mime="text/plain",
            )

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.markdown('<div class="footer-text">Distill — AI Summarization Engine</div>', unsafe_allow_html=True)