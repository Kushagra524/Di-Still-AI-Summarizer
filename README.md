# 🚀 Distill — AI-Powered RAG Summarization Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge&logo=streamlit"/>
</p>

---

# 🌌 Overview

**Distill** is a modern AI-powered RAG (Retrieval-Augmented Generation) summarization engine that transforms webpages, blogs, research papers, and YouTube videos into structured, intelligent summaries in seconds.

Built using:

- ⚡ Groq LLM Inference
- 🔗 LangChain
- 🧠 Recursive Chunking + Refinement
- 🎨 Advanced Streamlit UI
- 📚 Multi-source document ingestion

This project focuses on:
- Long-form content understanding
- AI-assisted learning
- Research summarization
- Technical documentation digestion
- Educational productivity

---

# ✨ Features

## 🧠 Advanced RAG Pipeline
- Recursive text chunking
- Multi-stage refinement summarization
- Context-aware summarization
- Streaming LLM responses
- Adaptive processing for small & large documents

---

## 🌍 Multi-Source Support

### ✅ Supported Sources
- Research Papers
- Technical Blogs
- Documentation
- Articles
- Educational Websites
- YouTube Videos

---

## ⚡ Ultra-Fast LLM Inference
Powered by:

```python
meta-llama/llama-4-scout-17b-16e-instruct
```

Benefits:
- Low latency generation
- Fast streaming responses
- High-quality structured summaries

---

## 🎨 Modern Futuristic UI
Custom-built Streamlit interface featuring:
- Glassmorphism design
- Animated gradients
- Dynamic glowing effects
- Real-time streaming summaries
- Downloadable outputs
- Responsive layout

---

## 📦 Export Support
Users can:
- Generate summaries instantly
- Download summaries as `.txt`
- Save structured learning notes

---

# 🏗️ System Architecture

```text
                ┌────────────────────┐
                │   User URL Input   │
                └─────────┬──────────┘
                          │
                          ▼
              ┌──────────────────────┐
              │  Content Extraction  │
              │ Webpage / YouTube    │
              └─────────┬────────────┘
                        │
                        ▼
             ┌───────────────────────┐
             │ Recursive Text Split  │
             │ Chunking Pipeline     │
             └─────────┬─────────────┘
                       │
                       ▼
             ┌───────────────────────┐
             │ Intermediate Summaries│
             │ LangChain + Groq      │
             └─────────┬─────────────┘
                       │
                       ▼
             ┌───────────────────────┐
             │ Refinement Pipeline   │
             │ Final Structured RAG  │
             └─────────┬─────────────┘
                       │
                       ▼
             ┌───────────────────────┐
             │ Final AI Summary      │
             └───────────────────────┘
```

---

# 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core backend |
| Streamlit | Frontend UI |
| LangChain | LLM orchestration |
| Groq API | Ultra-fast inference |
| BeautifulSoup | Web scraping |
| YouTubeLoader | Video transcript extraction |
| RecursiveCharacterTextSplitter | Document chunking |
| dotenv | Environment variable management |

---

# 📂 Project Structure

```bash
Distill/
│
├── app.py
├── requirements.txt
├── .env
├── README.md
│
└── assets/
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/distill-rag.git
cd distill-rag
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 🧠 How The RAG Pipeline Works

## Step 1 — URL Ingestion
The user submits:
- Webpage URL
- Blog URL
- YouTube URL

---

## Step 2 — Content Extraction
The system extracts:
- Visible webpage text
- YouTube transcripts
- Research content

Noise like:
- scripts
- headers
- footers
- navigation bars

is automatically removed.

---

## Step 3 — Recursive Chunking
Large documents are split into manageable chunks using:

```python
RecursiveCharacterTextSplitter
```

Benefits:
- Better context preservation
- Reduced token overload
- Efficient summarization

---

## Step 4 — Intermediate Summarization
Each chunk is independently summarized using:
- LangChain
- Groq LLM

---

## Step 5 — Refinement Chain
All partial summaries are recursively merged into:
- One coherent
- Structured
- Educational final summary

---

# 🎯 Key Highlights

✅ Handles extremely large documents  
✅ Streaming AI responses  
✅ Beautiful modern UI  
✅ Modular architecture  
✅ Production-style RAG workflow  
✅ Optimized for educational content  
✅ Downloadable summaries  
✅ Fast inference using Groq  

---

# 📸 UI Preview

## 🌌 Hero Section
- Futuristic gradient UI
- Animated glowing effects
- Premium typography

## 📝 Summary Section
- Structured output
- Live streaming text
- Statistics:
  - Word count
  - Character count
  - Source type

---

# 🚀 Future Improvements

- PDF Upload Support
- Semantic Vector Search
- ChromaDB / FAISS Integration
- Multi-document RAG
- Citation-aware summarization
- User authentication
- History management
- AI-generated flashcards
- Voice summarization

---

# 🧪 Example Use Cases

## 📚 Students
Summarize:
- Research papers
- Lecture material
- Documentation

---

## 👨‍💻 Developers
Digest:
- Technical blogs
- API docs
- Framework tutorials

---

## 🧠 Researchers
Understand:
- Long reports
- Academic content
- Whitepapers

---

# 🔥 Why This Project Stands Out

Unlike traditional summarizers, Distill:
- Uses a true RAG-style pipeline
- Handles long-context intelligently
- Maintains structural coherence
- Streams responses in real-time
- Focuses on educational summarization quality

---

# 🤝 Contributing

Contributions are welcome.

1. Fork repository
2. Create feature branch
3. Commit changes
4. Open Pull Request

---

# 📜 License

MIT License

---

# 👨‍💻 Developer

### Kushagra Srivastava

AI/ML • RAG Systems • LLM Applications • Generative AI • LangChain • Streamlit • Python

---

# ⭐ Support

If you like this project:

⭐ Star the repository  
🍴 Fork the project  
🚀 Build something powerful with it

---

# 💡 Final Note

Distill is more than a summarizer.

It is a scalable foundation for building:
- AI research assistants
- Knowledge engines
- Educational copilots
- Long-context AI systems
- Production-grade RAG applications

---
