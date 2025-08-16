# Alternative TTS Services Configuration

import os
from dotenv import load_dotenv

load_dotenv()

def get_available_tts_service():
    """
    Check which TTS service is available and return the preferred one.
    
    Returns:
        str: 'elevenlabs', 'openai', or 'offline'
    """
    elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    
    # Prefer ElevenLabs if available
    if elevenlabs_key:
        return 'elevenlabs'
    elif openai_key:
        return 'openai'
    else:
        return 'offline'

def generate_tts_openai(text, output_path):
    """
    Generate TTS using OpenAI's API.
    
    Args:
        text (str): Text to convert to speech
        output_path (str): Path to save the audio file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  # Available voices: alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        
        response.stream_to_file(output_path)
        return True
        
    except Exception as e:
        print(f"OpenAI TTS error: {e}")
        return False

def generate_tts_offline(text, output_path):
    """
    Generate a simple beep sound for testing when no TTS service is available.
    
    Args:
        text (str): Text to convert to speech (ignored)
        output_path (str): Path to save the audio file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import wave
        import struct
        import math
        
        # Generate a simple tone for testing
        duration = max(3.0, len(text) * 0.1)  # Rough estimate: 0.1s per character
        sample_rate = 44100
        frequency = 440  # A4 note
        
        # Generate sine wave
        frames = []
        for i in range(int(duration * sample_rate)):
            sample = math.sin(2 * math.pi * frequency * i / sample_rate)
            frames.append(struct.pack('<h', int(sample * 32767)))
        
        # Write WAV file
        with wave.open(output_path.replace('.mp3', '.wav'), 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(frames))
        
        # Convert to MP3 if ffmpeg is available
        from . import compose_video
        ffmpeg_path, _ = compose_video.find_ffmpeg_path()
        if ffmpeg_path:
            import subprocess
            subprocess.run([
                ffmpeg_path, "-y", "-i", output_path.replace('.mp3', '.wav'),
                "-c:a", "mp3", "-b:a", "128k", output_path
            ], capture_output=True)
            # Clean up WAV file
            if os.path.exists(output_path.replace('.mp3', '.wav')):
                os.remove(output_path.replace('.mp3', '.wav'))
        
        return True
        
    except Exception as e:
        print(f"Offline TTS error: {e}")
        return False
