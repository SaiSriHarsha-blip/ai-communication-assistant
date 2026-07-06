# 🚀 MessagePilot

## AI Communication Assistant

MessagePilot is an AI-powered communication assistant that generates context-aware, platform-specific messages using Google Gemini. It combines deterministic intent detection with LLM-powered generation to create professional, platform-aware messages for everyday communication.

---

## 🌐 Live Demo

- **Frontend:** https://ai-communication-assistant-sri-harsha.vercel.app/
- **Backend API:** https://messagepilot-backend.onrender.com
- **Swagger API:** https://messagepilot-backend.onrender.com/docs

---

## ✨ Features

- AI-powered Message Generation
- Intent Detection
- Context Builder
- Prompt Routing
- Relationship Detection
- Tone Detection
- Multiple Message Variants
- Prompt Injection Protection
- Rate Limiting
- Security Headers
- Logging Middleware
- Global Exception Handling
- Responsive Next.js Frontend
- Cloud Deployment (Render + Vercel)

---

# 🏗 Architecture

MessagePilot follows a modular AI pipeline that separates deterministic analysis from LLM generation. This architecture improves reliability, reduces unnecessary LLM calls, and produces structured, context-aware responses.

## Workflow Diagram

![Architecture](architecture.png)

### Request Flow


User
  │
  ▼
Intent Detector
  │
  ▼
Context Builder
  │
  ├──────────────► Clarification (if required)
  │
  ▼
Prompt Router
  │
  ▼
Prompt Renderer
  │
  ▼
Message Generation Service
  │
  ▼
Gemini 2.5 Flash
  │
  ▼
Structured Response

## 🛠 Tech Stack

### Backend

-   Python
-   FastAPI
-   Google Gemini 2.5 Flash
-   Google GenAI SDK
-   Pydantic v2
-   Jinja2
-   SlowAPI
-   Uvicorn

### Frontend

-   Next.js
-   React
-   TypeScript
-   Tailwind CSS

### Deployment

-   GitHub
-   Render
-   Vercel

## 📁 Folder Structure


MessagePilot/
├── app/
│   ├── agents/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── prompts/
│   ├── security/
│   ├── services/
│   └── main.py
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── tests/
├── requirements.txt
├── .env.example
└── README.md


## 🔐 Security

-   Prompt Injection Detection
-   Rate Limiting
-   Security Headers
-   Global Exception Handling
-   Request Logging

## ⚙️ API Documentation


### Live

-   https://messagepilot-backend.onrender.com/docs

## Getting Started
**Prerequisites**
Python 3.10+
A Google AI Studio API Key (obtain one from Google AI Studio)
Installation
Clone the repository:

git clone https://github.com/SaiSriHarsha-blip/ai-communication-assistant.git
cd ai-communication-assistant
Create and activate a virtual environment:

python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
Install the dependencies:

pip install -r requirements.txt
Environment Variables
Create a .env file in the root directory and add your credentials:

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
Running the Application
Start the FastAPI development server:

uvicorn app.main:app --reload
Access the API Documentation:

Swagger UI: http://127.0.0.1:8000/docs


## 📊 Project Status

  Module                  Status
  ----------------------- --------
  Backend                 ✅
  Frontend                ✅
  Gemini Integration      ✅
  Security                ✅
  Deployment              ✅
  Advanced Agent Skills   🚧

## 🛣 Roadmap

### Phase 1 

-   Backend
-   Frontend
-   AI Integration
-   Deployment
-   Security

### Phase 2 

-   Advanced Agent Skills
-   Better Intent Detection
-   Conversation Memory

### Phase 3 

-   Voice Input
-   Voice Output
-   Speech-to-Text
-   Text-to-Speech

### Phase 4 

-   PDF Upload
-   DOCX Upload
-   File Analysis
-   Smart Document Messaging

### Phase 5 

-   WhatsApp
-   Gmail
-   Slack
-   Microsoft Teams
-   Outlook

## 💡 Future Improvements

-   Voice Assistant
-   PDF/DOCX/TXT Support
-   Document Upload & Processing
-   Multi-language Expansion
-   AI Personalization
-   Mobile App
-   RAG Integration

## 👨‍💻 Author

**Sri Harsha**

GitHub:
https://github.com/SaiSriHarsha-blip/ai-communication-assistant
