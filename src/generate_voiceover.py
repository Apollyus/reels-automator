
import os
import json
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import time
import sys

# Add src directory to path for imports
sys.path.append(os.path.dirname(__file__))
from cache_manager import get_story_cache_key, get_cache_paths, cache_exists, copy_from_cache, save_to_cache

load_dotenv()

def get_latest_story_file():
    """
    Gets the path to the latest story file in the 'stories' directory.

    Returns:
        str: The path to the latest story file, or None if the directory is empty.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    stories_dir = os.path.join(project_root, "stories")
    
    if not os.path.exists(stories_dir):
        return None

    files = [os.path.join(stories_dir, f) for f in os.listdir(stories_dir) if f.endswith(".json")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def generate_voiceover(story_data):
    """
    Generates voiceovers from a story using available TTS services.
    Creates a combined audio file with fallback support.

    Args:
        story_data (dict): The story to generate voiceovers for.
    
    Returns:
        dict: Paths to generated audio files or None if error.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    voices_dir = os.path.join(project_root, "voices")
    if not os.path.exists(voices_dir):
        os.makedirs(voices_dir)

    timestamp = int(time.time())
    combined_path = os.path.join(voices_dir, f"{timestamp}.mp3")
    
    # Check cache first
    cache_key = get_story_cache_key(story_data)
    cache_path = get_cache_paths(project_root, cache_key, "audio")
    
    if cache_exists(cache_path):
        print(f"🎯 Using cached audio file...")
        if copy_from_cache(cache_path, combined_path):
            print(f"✅ Cached voiceover copied to {combined_path}")
            return create_result_paths(combined_path)
        else:
            print("⚠️  Failed to copy from cache, generating new audio...")
    
    combined_text = f"{story_data['title']}. {story_data['story']}"
    
    # Try ElevenLabs first
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if api_key:
        if generate_elevenlabs_tts(combined_text, combined_path, api_key):
            # Save to cache
            save_to_cache(combined_path, cache_path)
            return create_result_paths(combined_path)
    
    # Try OpenAI TTS as fallback
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        print("ElevenLabs failed, trying OpenAI TTS...")
        if generate_openai_tts(combined_text, combined_path, openai_key):
            # Save to cache
            save_to_cache(combined_path, cache_path)
            return create_result_paths(combined_path)
    
    # Use offline fallback (test tone)
    print("All TTS services failed, using offline test audio...")
    if generate_offline_tts(combined_text, combined_path):
        # Save to cache
        save_to_cache(combined_path, cache_path)
        return create_result_paths(combined_path)
    
    return None

def generate_elevenlabs_tts(text, output_path, api_key):
    """Generate TTS using ElevenLabs API."""
    try:
        print("Generating voiceover with ElevenLabs...")
        elevenlabs = ElevenLabs(api_key=api_key)
        
        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
        )
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print(f"ElevenLabs voiceover saved to {output_path}")
        return True
    except Exception as e:
        print(f"ElevenLabs TTS error: {e}")
        return False

def generate_openai_tts(text, output_path, api_key):
    """Generate TTS using OpenAI API."""
    try:
        from openai import OpenAI
        
        print("Generating voiceover with OpenAI...")
        client = OpenAI(api_key=api_key)
        
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        
        response.stream_to_file(output_path)
        print(f"OpenAI voiceover saved to {output_path}")
        return True
    except Exception as e:
        print(f"OpenAI TTS error: {e}")
        return False

def generate_offline_tts(text, output_path):
    """Generate test audio for offline testing."""
    try:
        import wave
        import struct
        import math
        
        print("Generating test audio (offline mode)...")
        
        # Generate a simple tone for testing
        duration = max(5.0, len(text) * 0.1)  # Rough estimate
        sample_rate = 44100
        frequency = 440
        
        # Generate sine wave
        frames = []
        for i in range(int(duration * sample_rate)):
            sample = math.sin(2 * math.pi * frequency * i / sample_rate)
            frames.append(struct.pack('<h', int(sample * 32767)))
        
        # Write WAV file first
        wav_path = output_path.replace('.mp3', '.wav')
        with wave.open(wav_path, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(frames))
        
        # Convert to MP3 if possible
        try:
            from compose_video import find_ffmpeg_path
            ffmpeg_path, _ = find_ffmpeg_path()
            if ffmpeg_path:
                import subprocess
                subprocess.run([
                    ffmpeg_path, "-y", "-i", wav_path,
                    "-c:a", "mp3", "-b:a", "128k", output_path
                ], capture_output=True, check=True)
                os.remove(wav_path)
            else:
                # Just rename WAV to MP3 if no ffmpeg
                os.rename(wav_path, output_path)
        except:
            # Fallback: rename WAV to MP3
            if os.path.exists(wav_path):
                os.rename(wav_path, output_path)
        
        print(f"Test audio saved to {output_path}")
        return True
    except Exception as e:
        print(f"Offline TTS error: {e}")
        return False

def create_result_paths(combined_path):
    """Create result dictionary with all paths pointing to the same file."""
    return {
        'title': combined_path,
        'story': combined_path,
        'combined': combined_path
    }

if __name__ == "__main__":
    latest_story_file = get_latest_story_file()
    if latest_story_file:
        with open(latest_story_file, "r") as f:
            story_data = json.load(f)
        
        results = generate_voiceover(story_data)
        if results:
            print("\nVoiceover generation completed successfully!")
            print(f"Title audio: {results.get('title', 'Not generated')}")
            print(f"Story audio: {results.get('story', 'Not generated')}")
            print(f"Combined audio: {results.get('combined', 'Not generated')}")
        else:
            print("Failed to generate voiceovers.")
    else:
        print("No stories found to generate a voiceover for.")
