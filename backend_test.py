#!/usr/bin/env python3
"""
Backend API Testing for SmartSpeak Voice Assistant
Tests all voice-related endpoints and integrations
"""

import requests
import sys
import json
import base64
import io
from datetime import datetime
from pathlib import Path

class VoiceAssistantTester:
    def __init__(self, base_url="https://smartspeak-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details="", error=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        result = {
            "test_name": name,
            "success": success,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    Details: {details}")
        if error:
            print(f"    Error: {error}")

    def test_health_check(self):
        """Test basic API health check"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"Status: {response.status_code}, Message: {data.get('message', 'N/A')}"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_test("API Health Check", success, details)
            return success
            
        except Exception as e:
            self.log_test("API Health Check", False, error=str(e))
            return False

    def create_test_audio_file(self):
        """Create a simple test audio file (WAV format)"""
        try:
            # Create a simple WAV file with silence
            import wave
            import struct
            
            # WAV file parameters
            sample_rate = 16000
            duration = 1  # 1 second
            frequency = 440  # A4 note
            
            # Generate audio data
            frames = []
            for i in range(int(sample_rate * duration)):
                # Generate a simple sine wave
                value = int(32767 * 0.1 * (i % 100) / 100)  # Very quiet tone
                frames.append(struct.pack('<h', value))
            
            # Create WAV file in memory
            audio_buffer = io.BytesIO()
            with wave.open(audio_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(b''.join(frames))
            
            audio_buffer.seek(0)
            return audio_buffer.getvalue()
            
        except Exception as e:
            print(f"Warning: Could not create test audio file: {e}")
            # Return minimal WAV header as fallback
            return b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00\x80\x3e\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00'

    def test_transcribe_endpoint(self):
        """Test /api/voice/transcribe endpoint"""
        try:
            # Create test audio file
            audio_data = self.create_test_audio_file()
            
            files = {'file': ('test_audio.wav', audio_data, 'audio/wav')}
            response = requests.post(f"{self.api_url}/voice/transcribe", files=files, timeout=30)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                text = data.get('text', '')
                details = f"Status: {response.status_code}, Transcribed text length: {len(text)}"
            else:
                try:
                    error_data = response.json()
                    details = f"Status: {response.status_code}, Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details = f"Status: {response.status_code}, Response: {response.text[:200]}"
                    
            self.log_test("Voice Transcribe Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice Transcribe Endpoint", False, error=str(e))
            return False

    def test_process_endpoint(self):
        """Test /api/voice/process endpoint"""
        try:
            payload = {
                "text": "What is Python programming?",
                "session_id": "test-session-123",
                "language": "en"
            }
            
            response = requests.post(
                f"{self.api_url}/voice/process", 
                json=payload, 
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                response_text = data.get('response', '')
                details = f"Status: {response.status_code}, Response length: {len(response_text)}"
            else:
                try:
                    error_data = response.json()
                    details = f"Status: {response.status_code}, Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details = f"Status: {response.status_code}, Response: {response.text[:200]}"
                    
            self.log_test("Voice Process Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice Process Endpoint", False, error=str(e))
            return False

    def test_speak_endpoint(self):
        """Test /api/voice/speak endpoint"""
        try:
            payload = {
                "text": "Hello, this is a test message.",
                "voice": "nova"
            }
            
            response = requests.post(
                f"{self.api_url}/voice/speak", 
                json=payload, 
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                audio_data = data.get('audio', '')
                details = f"Status: {response.status_code}, Audio data length: {len(audio_data)}"
            else:
                try:
                    error_data = response.json()
                    details = f"Status: {response.status_code}, Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details = f"Status: {response.status_code}, Response: {response.text[:200]}"
                    
            self.log_test("Voice Speak Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice Speak Endpoint", False, error=str(e))
            return False

    def test_voice_ask_endpoint(self):
        """Test /api/voice/ask endpoint (full flow)"""
        try:
            # Create test audio file
            audio_data = self.create_test_audio_file()
            
            files = {'file': ('test_audio.wav', audio_data, 'audio/wav')}
            data = {'language': 'en'}
            
            response = requests.post(
                f"{self.api_url}/voice/ask", 
                files=files, 
                data=data,
                timeout=60  # Longer timeout for full flow
            )
            
            success = response.status_code == 200
            
            if success:
                response_data = response.json()
                text = response_data.get('text', '')
                audio = response_data.get('audio', '')
                details = f"Status: {response.status_code}, Text length: {len(text)}, Audio length: {len(audio)}"
            else:
                try:
                    error_data = response.json()
                    details = f"Status: {response.status_code}, Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details = f"Status: {response.status_code}, Response: {response.text[:200]}"
                    
            self.log_test("Voice Ask Endpoint (Full Flow)", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice Ask Endpoint (Full Flow)", False, error=str(e))
            return False

    def test_history_endpoint(self):
        """Test /api/voice/history endpoint"""
        try:
            session_id = "test-session-123"
            response = requests.get(f"{self.api_url}/voice/history/{session_id}", timeout=10)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                messages = data.get('messages', [])
                details = f"Status: {response.status_code}, Messages count: {len(messages)}"
            else:
                try:
                    error_data = response.json()
                    details = f"Status: {response.status_code}, Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details = f"Status: {response.status_code}, Response: {response.text[:200]}"
                    
            self.log_test("Voice History Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice History Endpoint", False, error=str(e))
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting SmartSpeak Voice Assistant Backend Tests")
        print(f"🔗 Testing API at: {self.api_url}")
        print("=" * 60)
        
        # Test basic connectivity first
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return False
        
        # Test individual endpoints
        self.test_transcribe_endpoint()
        self.test_process_endpoint()
        self.test_speak_endpoint()
        self.test_history_endpoint()
        
        # Test full flow
        self.test_voice_ask_endpoint()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed - check details above")
        
        return self.tests_passed == self.tests_run

    def get_test_results(self):
        """Get detailed test results"""
        return {
            "total_tests": self.tests_run,
            "passed_tests": self.tests_passed,
            "success_rate": (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0,
            "test_details": self.test_results
        }


def main():
    """Main test execution"""
    tester = VoiceAssistantTester()
    
    try:
        success = tester.run_all_tests()
        
        # Save detailed results
        results = tester.get_test_results()
        with open('/app/backend_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())