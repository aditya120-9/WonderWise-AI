# 🌍 WonderWise AI – Intelligent Travel Assistant

A modern, **locally-hosted** AI-powered travel assistant that provides personalized travel recommendations, itineraries, and budget planning. Built with a **FastAPI backend**, **React frontend**, and **open-source LLM (Ollama)** for complete privacy and control.

---

## 🎯 Overview

WonderWise AI is a full-stack travel planning application that leverages a local language model (qwen2.5:3b) to deliver:
- **Smart Travel Itineraries** — Multi-day trip planning with source-backed pricing when verified data is available
- **Budget-Aware Recommendations** — Stays within user-specified budgets
- **Real-Time Streaming** — Live response generation via WebSocket
- **Conversation Memory** — Context-aware recommendations across sessions
- **RAG Integration** — Retrieval-Augmented Generation for factual travel data
- **Professional UI** — Clean, responsive React + Tailwind design

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Local LLM** | Runs qwen2.5:3b via Ollama—no cloud API costs, full privacy |
| 💬 **WebSocket Streaming** | Real-time response streaming for fast user feedback |
| 📍 **Budget Guidance** | AI checks arithmetic and labels prices as verified, estimated, or unverified |
| 🗣️ **Conversation Memory** | SQLite-based history for multi-turn context |
| 📚 **RAG System** | Retrieval-Augmented Generation with Chroma vector DB |
| 🎨 **Responsive UI** | React + TypeScript + Tailwind CSS for mobile & desktop |
| ⚡ **Fast Inference** | Optimized prompts and context size for ~2s response times |
| 📊 **Structured Output** | Bullet-point, point-wise responses for clarity |

---

## 🛠 Tech Stack

### Backend
- **FastAPI** — High-performance REST API & WebSocket server
- **LangChain** — LLM orchestration and RAG pipeline
- **Ollama** — Local large language model runtime (qwen2.5:3b)
- **Chroma** — Vector database for knowledge retrieval
- **SQLAlchemy** — ORM for conversation history storage
- **Python 3.12+** — Async-first backend

### Frontend
- **React 19** — UI framework with hooks
- **TypeScript** — Type-safe development
- **Vite** — Lightning-fast dev server & build tool
- **Tailwind CSS** — Utility-first styling
- **React Markdown** — Professional markdown rendering
- **WebSocket Client** — Real-time bidirectional communication

### Infrastructure
- **Windows PowerShell** — Automated startup script
- **Python Virtual Environment** — Isolated dependency management
- **Uvicorn** — ASGI server for FastAPI

---

## 📦 Installation & Setup

### Prerequisites
- **Python 3.12+** (with pip)
- **Node.js 18+** (with npm)
- **Ollama** installed and running (download from [ollama.ai](https://ollama.ai))
- **qwen2.5:3b** model downloaded: `ollama pull qwen2.5:3b`

### Step 1: Clone & Navigate
```bash
cd "Wonderwise Ai"
```

### Step 2: Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt -r requirements-phase2.txt -r requirements-dev.txt
```

### Step 3: Download the LLM Model
```bash
ollama pull qwen2.5:3b
ollama serve  # Keep Ollama running in a separate terminal (default: http://localhost:11434)
```

### Travel data and price confidence

The assistant does not treat model knowledge as live travel data. Add dated, trusted documents to `knowledge/` and run the ingestion command before expecting source-backed prices:

```bash
cd backend
python -m app.rag.ingest
```

Without retrieved source documents, the assistant labels prices as **Not verified** and does not invent numeric fares. Travel prices and availability should still be confirmed with the operator or property for the user's dates.

### Step 4: Frontend Setup
```bash
cd frontend\frontend

# Install dependencies
npm install
```

### Step 5: Start Both Services

#### Option A: Single Command (Recommended)
```bash
# From project root
powershell -ExecutionPolicy Bypass -File .\run-dev.ps1
```

#### Option B: Manual Start
```bash
# Terminal 1: Backend
cd backend
.venv\Scripts\activate
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend
cd frontend\frontend
npm run dev
```

### Step 6: Access the Application
- **Frontend**: `http://127.0.0.1:5173`
- **Backend API**: `http://127.0.0.1:8000`
- **Backend Docs**: `http://127.0.0.1:8000/docs`

---

## 🎮 Usage

### Chat Interface
1. Open `http://127.0.0.1:5173` in your browser
2. Type a travel query:
   - "2-day trip to Darjeeling with INR 5000 budget"
   - "Top 5 places to visit in eastern India"
   - "Kerala backwater cruise itinerary for 5 days"
3. Receive structured bullet-point responses with:
    - 🏨 Accommodation recommendations with source-backed prices when available
    - 🍽️ Food & dining suggestions with confidence labels
    - 🚗 Transport options and source-backed costs when available
   - 📍 Activities and attractions
   - 💰 Budget summary

### API Endpoints

#### HTTP Chat (Non-streaming)
```bash
POST /chat
Content-Type: application/json

{
  "message": "2-day Goa trip under INR 8000",
  "conversation_id": 1
}
```

#### WebSocket Chat (Streaming)
```
WS ws://127.0.0.1:8000/ws/chat
Message: { "message": "...", "conversation_id": 1 }
Response: { "type": "chunk", "content": "..." }
          { "type": "end" }
```

#### Health Check
```bash
GET /
Response: { "status": "running" }
```

#### Operations

```text
GET /health   # process liveness
GET /ready    # database and Ollama readiness
GET /metrics  # in-process latency and cache counters
```

#### Authentication

```text
POST /auth/register
POST /auth/login
GET  /conversations
POST /conversations
```

Chat requires a bearer token and an owned conversation. Exact current fares, availability, and prices require reviewed documents in `knowledge/` or configured live provider integrations; the model will not invent them.

---

## 🏗 Architecture

### System Flow
```
User Input (Frontend)
    ↓
React Chat UI
    ↓
WebSocket /ws/chat
    ↓
Backend StreamService
    ↓
Memory Service (load conversation history)
    ↓
RAG Retriever (Chroma vector DB)
    ↓
System Prompt + Context Assembly
    ↓
LangChain ChatOllama (qwen2.5:3b via Ollama)
    ↓
Streaming Response → WebSocket
    ↓
Frontend useChat Hook (real-time display)
    ↓
Markdown Rendering + UI Display
```

### Directory Structure
```
wonderwise ai/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── requirements.txt           # Python dependencies
│   ├── .venv/                     # Virtual environment
│   └── app/
│       ├── api/
│       │   ├── chat.py           # HTTP chat endpoint
│       │   └── websocket.py      # WebSocket streaming
│       ├── config/
│       │   └── settings.py       # Configuration (model, API URLs)
│       ├── database/
│       │   ├── database.py       # SQLAlchemy setup
│       │   └── models.py         # Message model
│       ├── llm/
│       │   └── ollama_client.py  # ChatOllama initialization
│       ├── memory/
│       │   └── memory_service.py # Conversation history service
│       ├── prompts/
│       │   └── system_prompt.py  # System prompt definition
│       ├── rag/
│       │   ├── chroma.py         # Chroma vector store init
│       │   ├── ingest.py         # Knowledge base ingestion
│       │   └── retriever.py      # Retrieval logic
│       ├── schemas/
│       │   └── chat.py           # Pydantic models
│       └── services/
│           ├── chat_service.py    # Non-streaming chat logic
│           └── stream_service.py  # Streaming chat logic
│
├── frontend/frontend/
│   ├── package.json              # npm dependencies
│   ├── vite.config.ts            # Vite configuration
│   ├── tsconfig.json             # TypeScript config
│   ├── tailwind.config.js        # Tailwind setup
│   └── src/
│       ├── main.tsx              # React entry point
│       ├── App.tsx               # Main app component
│       ├── pages/
│       │   └── ChatPage.tsx      # Chat interface
│       ├── components/
│       │   ├── chat/
│       │   │   ├── ChatWindow.tsx     # Chat display
│       │   │   ├── MessageBubble.tsx  # Message renderer
│       │   │   ├── chatInput.tsx      # Input field
│       │   │   ├── TypingIndicator.tsx
│       │   │   └── WelcomeScreen.tsx
│       │   ├── layout/
│       │   │   ├── Header.tsx
│       │   │   └── Sidebar.tsx
│       │   └── common/
│       │       ├── Button.tsx
│       │       └── Loader.tsx
│       ├── hooks/
│       │   ├── useChat.ts         # Chat state management
│       │   ├── useWebSocket.ts    # WebSocket hook
│       │   └── useAutoScroll.ts
│       ├── services/
│       │   ├── api.ts             # Axios instance
│       │   ├── chatService.ts     # Chat API calls
│       │   └── websocket.ts       # WebSocket service
│       └── types/
│           ├── chat.ts            # TypeScript interfaces
│           └── socket.ts
│
├── chroma/                        # Vector store data
├── knowledge/                     # Knowledge base documents
├── run-dev.ps1                    # Windows startup script
└── README.md                      # This file
```

---

## ⚙️ Configuration

### Backend Configuration ([`backend/app/config/settings.py`](backend/app/config/settings.py))
```python
OLLAMA_MODEL = "qwen2.5:3b"           # Model name
OLLAMA_BASE_URL = "http://localhost:11434"  # Ollama endpoint
DATABASE_URL = "sqlite:///./chat.db"  # SQLite database
CHROMA_PATH = "./chroma"              # Vector store path
```

### Model Parameters ([`backend/app/llm/ollama_client.py`](backend/app/llm/ollama_client.py))
```python
temperature = 0.3       # Deterministic, focused responses
top_p = 0.85            # Nucleus sampling
num_predict = 180       # Max tokens (fast responses)
repeat_penalty = 1.06   # Discourage repetition
```

### System Prompt
The system prompt enforces:
- Bullet-point formatted responses
- Budget awareness and enforcement
- Realistic local pricing
- Concise, actionable recommendations
- Professional output structure

---

## 🚀 Development Workflow

### Frontend Hot Reload
```bash
cd frontend\frontend
npm run dev  # Auto-reloads on file changes
```

### Backend Auto-Reload
```bash
cd backend
.venv\Scripts\activate
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Production Build
```bash
# Frontend
cd frontend\frontend
npm run build  # Output: dist/

# Backend
# Use: uvicorn main:app --host 0.0.0.0 --port 8000 (remove --reload)
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Average Response Time** | ~2–3 seconds |
| **Model** | qwen2.5:3b (3B parameters) |
| **Token Context Size** | 180 tokens |
| **Memory Usage** | ~2–3 GB |
| **Supported Concurrency** | 5–10 concurrent users (local) |

---

## 🔒 Privacy & Local-First

- ✅ **No cloud APIs** — Everything runs locally
- ✅ **No data collection** — Conversations stored only in local SQLite
- ✅ **Open-source stack** — FastAPI, LangChain, React all OSS
- ✅ **Full control** — Modify prompts, models, and logic freely

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

This project is open-source and available under the MIT License.

---

## 🆘 Troubleshooting

### Issue: Backend won't start on port 8000
**Solution:** Check if port is in use:
```bash
Get-NetTCPConnection -LocalPort 8000 | Stop-Process -Force
```

### Issue: "No module named 'langchain_ollama'"
**Solution:** Reinstall requirements:
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Ollama connection error
**Solution:** Ensure Ollama is running:
```bash
ollama serve
```

### Issue: Model responses are generic/too long
**Solution:** Prompts are tuned for speed. Longer responses indicate high load—restart backend and retry.

---

## 📧 Support & Questions

For issues, suggestions, or questions:
- Open an issue on GitHub
- Check existing documentation
- Review the system prompt for customization options

---

## 🎉 Acknowledgments

- **Ollama** — Local LLM runtime
- **LangChain** — RAG & LLM orchestration
- **FastAPI** — Web framework
- **React** — UI framework
- **Tailwind CSS** — Styling framework

---

**Built with ❤️ for travel planning | Powered by Local AI**