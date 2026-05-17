# AI-Powered RAG Video Assistant

An intelligent Retrieval-Augmented Generation (RAG) system that allows users to semantically search course videos and instantly find where specific topics are taught using AI-powered embeddings and LLM-based responses.

Built using `bge-m3` embeddings, cosine similarity retrieval, Whisper-based subtitle chunking, and support for both local and cloud-based Large Language Models (LLMs), the system retrieves relevant video segments along with timestamps and generates contextual answers.

---

# Features

- Semantic video search using vector embeddings
- AI-powered question answering from course content
- Timestamp-aware responses
- Automatic subtitle chunk generation using Whisper
- Supports both local and cloud LLM inference
- Cosine similarity-based retrieval pipeline
- Metadata-aware chunk processing
- Modular and scalable RAG architecture
- Human-like contextual responses
- Easy integration with custom datasets and courses

---

# LLM Support

This project supports two different inference approaches:

| Model | Type | Description |
|---|---|---|
| `llama3.2` | Local LLM | Runs completely offline using Ollama. No API required, but requires local model setup and sufficient system resources. |
| `Gemini 2.5 Flash` | Cloud API | Uses Google Gemini API for faster and higher-quality responses without requiring local model hosting. |

### Local Inference (llama3.2 via Ollama)
- Fully offline execution
- No external API dependency
- Requires Ollama setup and local model download
- Higher system resource usage

### Cloud Inference (Gemini API)
- No local LLM required
- Faster response generation
- Better answer quality
- Requires Gemini API key integration

---

# Tech Stack

| Technology | Usage |
|---|---|
| Python | Backend |
| Ollama | Local LLM Runtime |
| Gemini API | Cloud Inference |
| bge-m3 | Embedding Model |
| OpenAI Whisper | Audio Transcription |
| Pandas | Data Processing |
| NumPy | Vector Operations |
| Scikit-learn | Cosine Similarity |
| Joblib | Embedding Storage |

---

# Project Architecture

```text
                    ┌─────────────────────┐
                    │   Course Videos     │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Audio Extraction    │
                    │ (Video → MP3)       │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Whisper Transcriber │
                    │  Subtitle Creation  │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Chunk Generation    │
                    │ + Metadata Storage  │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ bge-m3 Embeddings   │
                    │ Vector Creation     │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Cosine Similarity   │
                    │ Semantic Retrieval  │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Prompt Augmentation │
                    └─────────┬───────────┘
                              │
               ┌──────────────┴──────────────┐
               │                             │
               ▼                             ▼
     ┌──────────────────┐         ┌──────────────────┐
     │ llama3.2 Ollama  │         │ Gemini 2.5 Flash │
     │  Local Inference │         │   API Inference  │
     └────────┬─────────┘         └────────┬─────────┘
              │                              │
              └──────────────┬───────────────┘
                             ▼
                  ┌─────────────────────┐
                  │ AI Generated Answer │
                  │ + Relevant Timestamp│
                  └─────────────────────┘
```

---

# Folder Structure

```text
RAG-Project/
│
├── app/
│   ├── config.py
│   ├── process_incoming.py
│   ├── embedding.joblib
│
├── initial/
│   ├── audios/
│   ├── videos/
│   ├── jsons/
│   ├── process_video.py
│   ├── create_chunks.py
│   ├── read_chunks.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# How to Use This RAG AI Teaching Assistant on Your Own Data

This project allows you to build an AI-powered semantic search assistant for educational videos using Retrieval-Augmented Generation (RAG), embeddings, and Large Language Models (LLMs).

The system processes course videos, generates subtitle embeddings, retrieves semantically relevant chunks, and answers user queries with contextual timestamps and explanations.

---

# Workflow

```text
Videos
   ↓
Audio Extraction
   ↓
Whisper Transcription
   ↓
Chunk Generation
   ↓
Embedding Creation
   ↓
Vector Similarity Search
   ↓
Prompt Augmentation
   ↓
LLM Response Generation
```

---

# Step 1 — Add Your Videos

Move all your course or lecture videos into the `videos/` directory.

Example:

```text
initial/videos/
```

Recommended naming format:

```text
01_Introduction.mp4
02_HTML_Basics.mp4
03_Paragraph_Tags.mp4
```

---

# Step 2 — Convert Videos to MP3

Run:

```bash
python process_video.py
```

This extracts audio files into:

```text
initial/audios/
```

---

# Step 3 — Generate JSON Subtitle Chunks

Run:

```bash
python create_chunks.py
```

This step:
- transcribes audio using Whisper
- generates subtitle chunks
- stores metadata such as:
  - video title
  - lecture number
  - timestamps
  - subtitle text

Generated files are stored in:

```text
initial/jsons/
```

---

# Step 4 — Generate Embeddings

Run:

```bash
python read_chunks.py
```

This step:
- loads subtitle chunks
- generates semantic embeddings using `bge-m3`
- stores embeddings in a dataframe
- saves vector data as:

```text
embedding.joblib
```

---

# Step 5 — Run the RAG Inference Pipeline

Run:

```bash
python process_incoming.py
```

The system:
1. receives a user query
2. generates query embeddings
3. performs cosine similarity search
4. retrieves relevant chunks
5. augments the prompt
6. sends context to the selected LLM
7. generates a contextual answer with timestamps

---

# Example Queries

```text
Where is boilerplate code taught?
Which lecture explains the p tag?
Where are anchor elements discussed?
Which video covers HTML lists?
```

---

# Models Used

| Model | Purpose |
|---|---|
| `bge-m3` | Embedding generation |
| `llama3.2` | Local LLM inference |
| `Gemini 2.5 Flash` | Cloud-based inference |
| `Whisper` | Audio transcription |

---

# Key Highlights

- Implemented end-to-end RAG pipeline from scratch
- Integrated semantic retrieval with LLM reasoning
- Designed modular preprocessing and inference workflows
- Built timestamp-aware educational assistant for video-based learning
- Supports both local and cloud-based inference systems
- Demonstrates practical AI engineering concepts

---

# Recommended Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Ollama:

```bash
ollama serve
```

Pull required local models:

```bash
ollama pull bge-m3
ollama pull llama3.2
```

---

# Future Improvements

- Streamlit / React frontend
- FAISS or Qdrant integration
- Multi-course support
- Chat history and memory
- Web deployment
- Real-time indexing
- Authentication system

---

# Repository Purpose

This project was built to explore modern AI engineering concepts including:
- Retrieval-Augmented Generation (RAG)
- Embeddings and vector search
- Semantic similarity
- Prompt engineering
- Local and cloud LLM orchestration
- AI-powered educational search systems
- 
