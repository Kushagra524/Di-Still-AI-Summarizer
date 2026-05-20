"""
Drop this into your main Streamlit app file.
Call inject_styles() once at the top, before any other st.* calls.
"""

import streamlit as st


def inject_styles():
    st.markdown("""
<style>

/* ── Keyframe animations ───────────────────────────────────────── */

@keyframes rainbow-flow {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position:  200% center; }
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(139,92,246,0.45), 0 0 40px rgba(99,102,241,0.2); }
  50%       { box-shadow: 0 0 32px rgba(139,92,246,0.75), 0 0 64px rgba(99,102,241,0.4), 0 0 90px rgba(59,130,246,0.2); }
}

@keyframes orb-drift-1 {
  0%, 100% { transform: translate(0,0)   scale(1);    opacity: .15; }
  33%       { transform: translate(30px,-20px) scale(1.1); opacity: .25; }
  66%       { transform: translate(-20px,15px) scale(.95); opacity: .10; }
}

@keyframes orb-drift-2 {
  0%, 100% { transform: translate(0,0)   scale(1);    opacity: .10; }
  33%       { transform: translate(-40px,20px) scale(1.15); opacity: .20; }
  66%       { transform: translate(25px,-30px) scale(.90); opacity: .15; }
}

/* ── Page / app shell ───────────────────────────────────────────── */

.stApp {
    background: #080b14 !important;
}

/* hide default Streamlit header chrome */
header[data-testid="stHeader"] { background: transparent !important; }

/* ── Floating orb blobs (injected via HTML component) ──────────── */
/* See inject_orbs() below — Streamlit can't do ::before on body    */

/* ── Rainbow headline ───────────────────────────────────────────── */

.rainbow-text {
    display: inline-block;
    background: linear-gradient(
        90deg,
        #ff0080, #ff4d4d, #ffb347, #ffff66,
        #47ff8a, #47d4ff, #7b6cff, #e040fb,
        #ff0080, #ff4d4d, #ffb347, #ffff66
    );
    background-size: 300% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: rainbow-flow 3s linear infinite;
    filter: drop-shadow(0 0 18px rgba(139,92,246,.55));
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.1;
}

.headline-static {
    display: block;
    color: rgba(255,255,255,.92);
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.1;
}

/* ── Powered-by badge ───────────────────────────────────────────── */

.powered-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 16px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .09em;
    text-transform: uppercase;
    color: #c4b5fd;
    background: rgba(139,92,246,.12);
    border: 1px solid rgba(139,92,246,.30);
    margin-bottom: 24px;
}

.powered-badge::before {
    content: '';
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #8b5cf6;
    box-shadow: 0 0 8px #8b5cf6;
    animation: pulse-glow 2s ease-in-out infinite;
    display: inline-block;
}

/* ── URL input ──────────────────────────────────────────────────── */

/* Streamlit wraps inputs — target the inner <input> */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,.05) !important;
    border: 1px solid rgba(255,255,255,.10) !important;
    border-radius: 12px !important;
    color: rgba(255,255,255,.85) !important;
    padding: 14px 18px !important;
    font-size: 14px !important;
    transition: border-color .2s, background .2s !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(255,255,255,.25) !important;
}

div[data-testid="stTextInput"] input:focus {
    background: rgba(255,255,255,.07) !important;
    border-color: rgba(139,92,246,.55) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,.14) !important;
}

div[data-testid="stTextInput"] label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: .10em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,.35) !important;
}

/* ── Primary "Generate Summary" button ──────────────────────────── */

div[data-testid="stButton"] > button[kind="primary"],
div[data-testid="stButton"] > button {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #7c3aed, #4f46e5, #0ea5e9) !important;
    background-size: 200% 200% !important;
    animation: pulse-glow 3s ease-in-out infinite !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 14px 28px !important;
    transition: transform .15s, opacity .15s !important;
    letter-spacing: .02em !important;
}

/* shimmer sweep */
div[data-testid="stButton"] > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(255,255,255,.18) 50%,
        transparent 100%
    );
    background-size: 200% 100%;
    animation: shimmer 2.5s linear infinite;
    pointer-events: none;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    opacity: .94 !important;
}

div[data-testid="stButton"] > button:active {
    transform: scale(.97) !important;
}

/* ── Download button ────────────────────────────────────────────── */

div[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,.05) !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 12px !important;
    color: rgba(255,255,255,.70) !important;
    font-size: 14px !important;
    padding: 12px 20px !important;
    transition: all .2s !important;
}

div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(255,255,255,.09) !important;
    border-color: rgba(255,255,255,.22) !important;
    color: rgba(255,255,255,.90) !important;
    transform: translateY(-1px) !important;
}

/* ── Summary output box ─────────────────────────────────────────── */

.summary-box {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(139,92,246,.25);
    border-radius: 14px;
    padding: 24px 28px;
    color: rgba(255,255,255,.82);
    font-size: 15px;
    line-height: 1.75;
    margin-top: 20px;
}

/* ── Feature pills ──────────────────────────────────────────────── */

.feature-pills {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    margin-top: 20px;
    justify-content: center;
}

.feature-pill {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 6px 13px;
    border-radius: 999px;
    font-size: 12px;
    color: rgba(255,255,255,.45);
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
}

.dot { width:6px; height:6px; border-radius:50%; display:inline-block; }
.dot-purple { background:#8b5cf6; box-shadow: 0 0 6px #8b5cf6; }
.dot-cyan   { background:#06b6d4; box-shadow: 0 0 6px #06b6d4; }
.dot-green  { background:#10b981; box-shadow: 0 0 6px #10b981; }

/* ── Streamlit misc cleanup ─────────────────────────────────────── */

footer { display: none !important; }
#MainMenu { visibility: hidden; }

</style>
""", unsafe_allow_html=True)


def inject_orbs():
    """
    Injects the animated background orbs.
    Call this right after inject_styles(), before your main content.
    """
    st.markdown("""
<div style="position:fixed; inset:0; pointer-events:none; z-index:0; overflow:hidden;">
  <div style="
    position:absolute; width:340px; height:340px; border-radius:50%;
    background:radial-gradient(circle, rgba(139,92,246,.55), rgba(59,130,246,.25));
    filter:blur(70px); top:-100px; right:-60px;
    animation: orb-drift-1 9s ease-in-out infinite;
  "></div>
  <div style="
    position:absolute; width:280px; height:280px; border-radius:50%;
    background:radial-gradient(circle, rgba(236,72,153,.45), rgba(99,102,241,.25));
    filter:blur(65px); bottom:-70px; left:-50px;
    animation: orb-drift-2 11s ease-in-out infinite;
  "></div>
  <div style="
    position:absolute; width:200px; height:200px; border-radius:50%;
    background:radial-gradient(circle, rgba(6,182,212,.35), rgba(16,185,129,.2));
    filter:blur(55px); top:45%; left:-30px;
    animation: orb-drift-2 13s ease-in-out infinite reverse;
  "></div>
</div>
""", unsafe_allow_html=True)


def render_header():
    """Renders the styled hero headline + badge."""
    st.markdown("""
<div style="text-align:center; padding: 40px 0 8px; position:relative; z-index:1;">
  <div class="powered-badge">Powered by Groq + LangChain</div>
  <h1 style="margin:0; line-height:1.1;">
    <span class="headline-static">Extract what</span>
    <span class="headline-static">actually</span>
    <span class="rainbow-text">matters</span>
  </h1>
  <p style="color:rgba(255,255,255,.42); font-size:15px; margin-top:14px; line-height:1.6;">
    Paste any webpage or YouTube URL — get a precise, structured summary in seconds.
  </p>
  <div class="feature-pills">
    <span class="feature-pill"><span class="dot dot-purple"></span>YouTube &amp; Web</span>
    <span class="feature-pill"><span class="dot dot-cyan"></span>Long content handled</span>
    <span class="feature-pill"><span class="dot dot-green"></span>Download summary</span>
  </div>
</div>
""", unsafe_allow_html=True)


def render_summary(text: str):
    """Wraps the summary output in a styled box."""
    import html
    safe = html.escape(text).replace('\n', '<br>')
    st.markdown(f'<div class="summary-box">{safe}</div>', unsafe_allow_html=True)


# ── Example usage ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    st.set_page_config(page_title="Distill", page_icon="✦", layout="centered")

    inject_styles()
    inject_orbs()
    render_header()

    st.markdown("<div style='position:relative; z-index:1;'>", unsafe_allow_html=True)

    url = st.text_input("Source URL", placeholder="https://youtube.com/watch?v=...  or any webpage", label_visibility="visible")

    col1, col2 = st.columns([3, 1])
    with col1:
        generate = st.button("✦ Generate Summary", use_container_width=True)
    with col2:
        st.button("↺ Clear", use_container_width=True)

    if generate and url:
        with st.spinner("Summarizing…"):
            # ← plug in your existing summarization logic here
            summary = f"[Summary for {url} would appear here]"

        render_summary(summary)

        st.download_button(
            label="⬇ Download summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:rgba(255,255,255,.15); font-size:11px; margin-top:60px;'>Distill — AI Summarization Engine</p>", unsafe_allow_html=True)

    