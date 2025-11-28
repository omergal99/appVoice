# SmartSpeak - Architecture Documentation

## System Overview

SmartSpeak is a voice-powered AI assistant built with a modern, modular architecture that separates concerns cleanly across three main layers:

1. **Presentation Layer** (React Frontend)
2. **Application Layer** (FastAPI Backend)
3. **Integration Layer** (AI Services)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           VoiceAssistant Component                      │ │
│  │  - Audio Recording (MediaRecorder API)                 │ │
│  │  - Language Selection                                   │ │
│  │  - Conversation Display                                 │ │
│  │  - Audio Playback                                       │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   API Routes Layer                      │ │
│  │              /api/voice/transcribe                      │ │
│  │              /api/voice/process                         │ │
│  │              /api/voice/speak                          │ │
│  │              /api/voice/ask (complete flow)            │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│  ┌────────────┬────────────┴────────────┬─────────────────┐ │
│  │            │                         │                  │ │
│  │  Audio     │      AI Service        │   TTS Service    │ │
│  │  Service   │      (GPT-5.1)         │   (OpenAI TTS)   │ │
│  │ (Whisper)  │                         │                  │ │
│  └────────────┴─────────────────────────┴─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ emergentintegrations
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    External AI Services                      │
│  ┌──────────────┬──────────────────┬────────────────────┐  │
│  │   Whisper    │     GPT-5.1      │    OpenAI TTS      │  │
│  │ Speech-to-   │   Language       │  Text-to-Speech    │  │
│  │    Text      │     Model        │                    │  │
│  └──────────────┴──────────────────┴────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Layer

#### VoiceAssistant Component
**Location**: `/app/frontend/src/components/VoiceAssistant.jsx`

**Responsibilities**:
- Audio recording using MediaRecorder API
- Language selection (Auto, English, Hebrew)
- Conversation display (user messages and assistant responses)
- Audio playback for TTS responses
- State management for recording/processing status

**Key Features**:
- Real-time audio recording
- Automatic transcription on recording stop
- Smooth UI transitions and animations
- Error handling with toast notifications

### Backend Layer

#### Server (`server.py`)
**Location**: `/app/backend/server.py`

**Responsibilities**:
- FastAPI application setup
- CORS configuration
- MongoDB connection
- Route registration
- Logging configuration

#### API Routes (`voice_routes.py`)
**Location**: `/app/backend/routes/voice_routes.py`

**Endpoints**:
1. `POST /api/voice/transcribe` - Audio to text conversion
2. `POST /api/voice/process` - Query processing with AI
3. `POST /api/voice/speak` - Text to speech conversion
4. `POST /api/voice/ask` - Complete voice pipeline
5. `GET /api/voice/history/{session_id}` - Conversation history (future use)

### Service Layer

#### Audio Service (`audio_service.py`)
**Location**: `/app/backend/services/audio_service.py`

**Responsibilities**:
- Initialize OpenAI Whisper client
- Transcribe audio files to text
- Handle language detection
- Error handling for audio processing

**Key Methods**:
```python
async def transcribe_audio(audio_data: bytes, language: str = None) -> dict
```

#### AI Service (`ai_service.py`)
**Location**: `/app/backend/services/ai_service.py`

**Responsibilities**:
- Initialize GPT-5.1 chat client
- Process user queries with context
- Generate intelligent responses
- Multilingual support (English/Hebrew)

**Key Methods**:
```python
async def process_query(query: str, session_id: str, language: str = "en") -> str
```

**System Messages**:
- English: Technical assistant specializing in programming, architecture, cloud, and security
- Hebrew: Same expertise in Hebrew language

#### TTS Service (`tts_service.py`)
**Location**: `/app/backend/services/tts_service.py`

**Responsibilities**:
- Initialize OpenAI TTS client
- Convert text to natural speech
- Return base64-encoded audio
- Support multiple voices

**Key Methods**:
```python
async def text_to_speech(text: str, voice: str = "nova") -> str
```

### Data Models

#### Conversation Models (`conversation.py`)
**Location**: `/app/backend/models/conversation.py`

**Models**:
1. `Message`: Single message in a conversation
2. `Conversation`: Complete conversation session
3. `ConversationCreate`: Request model for new conversations

## Data Flow

### Complete Voice Interaction Flow

```
User Speaks
    │
    ▼
[1] Frontend Records Audio (MediaRecorder)
    │
    ▼
[2] Audio Blob Created
    │
    ▼
[3] POST /api/voice/transcribe
    │
    ▼
[4] AudioService.transcribe_audio()
    │
    ▼
[5] Whisper API (emergentintegrations)
    │
    ▼
[6] Text Returned to Frontend
    │
    ▼
[7] POST /api/voice/process
    │
    ▼
[8] AIService.process_query()
    │
    ▼
[9] GPT-5.1 API (emergentintegrations)
    │
    ▼
[10] AI Response Returned
    │
    ▼
[11] POST /api/voice/speak
    │
    ▼
[12] TTSService.text_to_speech()
    │
    ▼
[13] OpenAI TTS API (emergentintegrations)
    │
    ▼
[14] Base64 Audio Returned
    │
    ▼
[15] Frontend Plays Audio
    │
    ▼
User Hears Response
```

## Security Considerations

### API Key Management
- All API keys stored in environment variables
- Never hardcoded in source code
- Easy to rotate keys by updating `.env` file

### CORS Configuration
- Configured to allow necessary origins
- Can be restricted for production use

### Input Validation
- File upload validation for audio files
- Request body validation using Pydantic models
- Error handling at all layers

## Scalability Considerations

### Current Implementation
- Single server deployment
- Synchronous audio processing
- In-memory conversation state

### Future Enhancements
1. **Horizontal Scaling**: Deploy multiple backend instances behind load balancer
2. **Async Processing**: Use message queues (RabbitMQ/Redis) for audio processing
3. **Database Integration**: Store conversations in MongoDB
4. **Caching**: Cache frequent queries and responses
5. **CDN**: Serve static audio files from CDN
6. **Rate Limiting**: Protect APIs from abuse

## Monitoring & Logging

### Current Logging
- Application logs via Python logging module
- Request/response logging in FastAPI
- Error tracking with stack traces

### Future Monitoring
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Usage analytics
- API response time metrics

## Deployment Architecture

### Current Setup
- Kubernetes container environment
- Backend: FastAPI on port 8002
- Frontend: React on port 3000
- MongoDB: Local instance
- Supervisor for process management

### Production Recommendations
1. **Container Orchestration**: Kubernetes or Docker Swarm
2. **Database**: Managed MongoDB (Atlas) or PostgreSQL
3. **Load Balancing**: NGINX or cloud load balancer
4. **SSL/TLS**: Let's Encrypt certificates
5. **CDN**: CloudFlare or AWS CloudFront
6. **Monitoring**: Prometheus + Grafana

## Technology Choices & Rationale

### Backend: FastAPI
**Why?**
- Modern, fast Python web framework
- Automatic API documentation (OpenAPI)
- Native async/await support
- Type hints and validation with Pydantic

### Frontend: React 19
**Why?**
- Component-based architecture
- Large ecosystem and community
- Excellent for interactive UIs
- Good TypeScript support

### AI Integration: emergentintegrations
**Why?**
- Unified interface for multiple AI providers
- Built-in error handling
- Optimized for LLM usage
- Easy provider switching

### Database: MongoDB
**Why?**
- Flexible schema for conversation data
- Fast document queries
- Easy to scale horizontally
- Good for unstructured data

## Code Quality Standards

### Backend
- Type hints for all functions
- Async/await for I/O operations
- Error handling at every layer
- Logging for debugging
- Pydantic models for validation

### Frontend
- Functional components with hooks
- PropTypes or TypeScript for type checking
- Error boundaries for error handling
- Accessibility considerations
- Responsive design

## Testing Strategy

### Backend Testing
- Unit tests for services
- Integration tests for API endpoints
- Mock external API calls in tests

### Frontend Testing
- Component unit tests
- Integration tests for user flows
- E2E tests with Playwright

### Manual Testing
- Voice recording and playback
- Multi-language support
- Error scenarios
- Edge cases

## Future Architecture Enhancements

1. **Microservices**: Split into separate services (auth, voice, ai)
2. **Event-Driven**: Use message queues for async processing
3. **Multi-Tenant**: Support multiple users with isolation
4. **Real-Time**: WebSocket support for live conversations
5. **Mobile Apps**: Native iOS/Android apps
6. **Voice Training**: Custom voice models per user
7. **Analytics Dashboard**: Usage statistics and insights

## Contributing Guidelines

When adding new features:
1. Keep services modular and single-purpose
2. Add type hints and validation
3. Write tests for new functionality
4. Update documentation
5. Follow existing code style
6. Add logging for debugging

---

**Last Updated**: November 2025
**Version**: 1.0.0
