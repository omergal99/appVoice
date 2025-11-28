import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Volume2, Loader2 } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const VoiceAssistant = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversation, setConversation] = useState([]);
  const [language, setLanguage] = useState('auto');
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await processVoice(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorder.start();
      setIsRecording(true);
      
    } catch (error) {
      console.error('Error accessing microphone:', error);
      toast.error('Failed to access microphone');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processVoice = async (audioBlob) => {
    setIsProcessing(true);
    
    try {
      // Step 1: Transcribe
      const formData = new FormData();
      formData.append('file', audioBlob, 'audio.webm');
      
      const transcribeRes = await axios.post(`${API}/voice/transcribe`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      const userText = transcribeRes.data.text;
      
      // Add user message to conversation
      setConversation(prev => [...prev, { role: 'user', content: userText }]);
      
      // Step 2: Process with AI
      const processRes = await axios.post(`${API}/voice/process`, {
        text: userText,
        session_id: 'demo-session',
        language: language === 'auto' ? 'en' : language
      });
      
      const assistantText = processRes.data.response;
      
      // Add assistant message to conversation
      setConversation(prev => [...prev, { role: 'assistant', content: assistantText }]);
      
      // Step 3: Text-to-Speech
      const ttsRes = await axios.post(`${API}/voice/speak`, {
        text: assistantText,
        voice: 'nova'
      });
      
      // Play audio
      const audioSrc = `data:audio/mp3;base64,${ttsRes.data.audio}`;
      if (audioRef.current) {
        audioRef.current.src = audioSrc;
        audioRef.current.play();
      }
      
    } catch (error) {
      console.error('Voice processing error:', error);
      toast.error('Failed to process voice');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="voice-assistant-container">
      <audio ref={audioRef} />
      
      {/* Header */}
      <div className="assistant-header">
        <h1 className="assistant-title">SmartSpeak</h1>
        <p className="assistant-subtitle">Your Intelligent Voice Assistant</p>
      </div>

      {/* Language Selector */}
      <div className="language-selector">
        <Button
          data-testid="lang-auto-btn"
          variant={language === 'auto' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setLanguage('auto')}
        >
          Auto
        </Button>
        <Button
          data-testid="lang-en-btn"
          variant={language === 'en' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setLanguage('en')}
        >
          English
        </Button>
        <Button
          data-testid="lang-he-btn"
          variant={language === 'he' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setLanguage('he')}
        >
          עברית
        </Button>
      </div>

      {/* Conversation Display */}
      <div className="conversation-container">
        {conversation.length === 0 ? (
          <div className="empty-state">
            <Volume2 className="empty-icon" size={48} />
            <p>Start a conversation by pressing the microphone button</p>
          </div>
        ) : (
          <div className="messages-list">
            {conversation.map((msg, idx) => (
              <Card 
                key={idx} 
                className={`message-card ${msg.role}`}
                data-testid={`message-${msg.role}-${idx}`}
              >
                <div className="message-content">{msg.content}</div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Microphone Button */}
      <div className="mic-button-container">
        {isProcessing ? (
          <Button 
            data-testid="processing-btn"
            className="mic-button processing" 
            size="lg" 
            disabled
          >
            <Loader2 className="animate-spin" size={32} />
          </Button>
        ) : isRecording ? (
          <Button
            data-testid="stop-recording-btn"
            className="mic-button recording"
            size="lg"
            onClick={stopRecording}
          >
            <MicOff size={32} />
          </Button>
        ) : (
          <Button
            data-testid="start-recording-btn"
            className="mic-button"
            size="lg"
            onClick={startRecording}
          >
            <Mic size={32} />
          </Button>
        )}
        
        {isRecording && (
          <p className="recording-indicator" data-testid="recording-indicator">
            Recording...
          </p>
        )}
      </div>
    </div>
  );
};

export default VoiceAssistant;
