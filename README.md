# SmartSpeak - Intelligent Voice Assistant

A professional voice-powered AI assistant specialized in answering technical questions about programming, architecture, cloud, and cybersecurity.

### Installing Dependencies

#### Backend
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements.local.txt
```

#### Frontend
```bash
cd frontend
yarn install
```

### Running the Application

#### Backend
```bash
cd backend
if needed (. .venv/bin/activate) (.\venv\Scripts\activate)
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

#### Frontend
```bash
cd frontend
yarn start
```

# appVoice

for freview flow use "Mermaid Preview" vscode extension
https://marketplace.visualstudio.com/items?itemName=vstirbu.vscode-mermaid-preview



## Features

### Core Capabilities
- **Speech-to-Text**: Uses OpenAI Whisper for accurate audio transcription
- **Intelligent Processing**: GPT-5.1 processes queries with technical expertise
- **Text-to-Speech**: Natural voice responses using OpenAI TTS
- **Multilingual Support**: Works with English and Hebrew
- **Technical Focus**: Specialized in developer and tech questions

### Architecture Highlights
- **Modular Design**: Clean separation of concerns with dedicated services
- **Environment-Based Configuration**: All API keys managed through environment variables
- **Real-time Processing**: Fast voice-to-response pipeline
- **Modern UI**: Beautiful gradient design with glassmorphism effects

## Project Structure

```
/app/
├── backend/
│   ├── server.py                 # FastAPI main application
│   ├── models/
│   │   └── conversation.py       # Data models
│   ├── services/
│   │   ├── audio_service.py      # Whisper integration
│   │   ├── ai_service.py         # GPT-5.1 integration
│   │   └── tts_service.py        # Text-to-Speech integration
│   ├── routes/
│   │   └── voice_routes.py       # API endpoints
│   └── .env                      # Environment variables
└── frontend/
    ├── src/
    │   ├── App.js                # Main React component
    │   ├── App.css               # Styling
    │   └── components/
    │       └── VoiceAssistant.jsx # Voice assistant UI
    └── package.json              # Dependencies
```

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **OpenAI Whisper**: Speech-to-text transcription
- **GPT-5.1**: Advanced language model for query processing
- **OpenAI TTS**: High-quality text-to-speech
- **MongoDB**: Database for future conversation history
- **emergentintegrations**: Unified API for AI services

### Frontend
- **React 19**: Latest React version
- **Shadcn/UI**: Beautiful, accessible components
- **Lucide Icons**: Modern icon library
- **MediaRecorder API**: Browser audio recording
- **Axios**: HTTP client

## API Endpoints

### Voice Assistant Endpoints

#### `GET /api/`
Health check endpoint
```bash
curl https://smartspeak-2.preview.emergentagent.com/api/
```

#### `POST /api/voice/transcribe`
Transcribe audio to text
```bash
curl -X POST https://smartspeak-2.preview.emergentagent.com/api/voice/transcribe \
  -F "file=@audio.webm"
```

#### `POST /api/voice/process`
Process query with AI
```bash
curl -X POST https://smartspeak-2.preview.emergentagent.com/api/voice/process \
  -H "Content-Type: application/json" \
  -d '{"text": "What is REST API?", "session_id": "demo", "language": "en"}'
```

#### `POST /api/voice/speak`
Convert text to speech
```bash
curl -X POST https://smartspeak-2.preview.emergentagent.com/api/voice/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is SmartSpeak", "voice": "nova"}'
```

#### `POST /api/voice/ask`
Complete voice flow (transcribe → process → speak)
```bash
curl -X POST "https://smartspeak-2.preview.emergentagent.com/api/voice/ask?language=en" \
  -F "file=@audio.webm"
```

## Setup & Configuration

### Environment Variables

#### Backend (`/app/backend/.env`)
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="voice_assistant_db"
CORS_ORIGINS="*"
EMERGENT_LLM_KEY=sk-emergent-2Ac2b01C9Ec9fF4Ac1
```

#### Frontend (`/app/frontend/.env`)
```env
REACT_APP_BACKEND_URL=https://smartspeak-2.preview.emergentagent.com
```

## Usage

1. **Open the Application**: Navigate to the frontend URL
2. **Select Language**: Choose Auto, English, or Hebrew
3. **Press Microphone Button**: Click the circular microphone button
4. **Speak Your Question**: Ask anything technical (e.g., "What is Docker?")
5. **Release Button**: Stop recording to process
6. **Listen to Response**: The AI will respond with voice

## Example Questions

### Programming
- "How do I implement BFS in JavaScript?"
- "What's the difference between REST and GraphQL?"
- "Explain async/await in Python"

### Architecture
- "What are the benefits of microservices?"
- "How to design a scalable system?"
- "Explain event-driven architecture"

### Cloud & DevOps
- "How to deploy on Kubernetes?"
- "What is serverless computing?"
- "Explain CI/CD pipelines"

### Cybersecurity
- "How to prevent SQL injection?"
- "What is XSS and how to defend against it?"
- "Explain zero-trust security"

## Switching API Keys

To use your own OpenAI API key instead of the Emergent LLM key:

1. Replace in `/app/backend/.env`:
```env
EMERGENT_LLM_KEY=your-openai-api-key-here
```

2. Restart the backend:
```bash
sudo supervisorctl restart backend
```

## Design Philosophy

- **Modular Code**: Each service handles one responsibility
- **Small Files**: Easy to maintain and understand
- **No Code Duplication**: DRY (Don't Repeat Yourself) principle
- **Clean Architecture**: Clear separation between layers
- **Environment-Based Config**: No hardcoded values

## Future Enhancements

- [ ] Persistent conversation history in MongoDB
- [ ] User authentication
- [ ] Custom voice training
- [ ] Multi-turn conversations with context
- [ ] Code execution sandbox
- [ ] Integration with development tools
- [ ] Real-time collaboration features

## Interview Highlights

When presenting this project in interviews:

1. **Technical Depth**: Shows knowledge of modern AI APIs and integration patterns
2. **Full-Stack Skills**: Backend (Python/FastAPI) + Frontend (React)
3. **Architecture**: Demonstrates clean, modular code organization
4. **Real-World Application**: Solves actual developer pain points
5. **Scalability**: Built with growth in mind
6. **Security**: Proper API key management
7. **UX/UI**: Professional, modern design

## License

MIT License - Free to use and modify

## Author

Built with passion for creating innovative voice-powered solutions.

---

**Demo**: [https://smartspeak-2.preview.emergentagent.com](https://smartspeak-2.preview.emergentagent.com)
