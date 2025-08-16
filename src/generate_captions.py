import os
import json
import re
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

def get_latest_voice_file():
    """
    Gets the path to the latest voice file in the 'voices' directory.

    Returns:
        str: The path to the latest voice file, or None if the directory is empty.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    voices_dir = os.path.join(project_root, "voices")
    
    if not os.path.exists(voices_dir):
        return None

    files = [os.path.join(voices_dir, f) for f in os.listdir(voices_dir) if f.endswith(".mp3")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def format_srt_time(seconds):
    """
    Formats seconds into SRT time format (HH:MM:SS,mmm).

    Args:
        seconds (float): Time in seconds.

    Returns:
        str: Formatted time string.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def generate_captions(story_data, voice_file_path, words_per_chunk=4):
    """
    Generates timed captions for a story using ElevenLabs forced alignment.

    Args:
        story_data (dict): The story data containing the text.
        voice_file_path (str): Path to the voiceover audio file.
        words_per_chunk (int): Number of words to display per caption (default: 4).
                              Use 1-2 for minimal text, 3-4 for balanced, 5-8 for more text.

    Returns:
        str: Path to the generated SRT file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    captions_dir = os.path.join(project_root, "captions")
    
    # Create captions directory if it doesn't exist
    if not os.path.exists(captions_dir):
        os.makedirs(captions_dir)
    
    # Generate output path
    voice_filename = os.path.basename(voice_file_path)
    srt_filename = voice_filename.replace('.mp3', '.srt')
    srt_path = os.path.join(captions_dir, srt_filename)
    
    # Check cache first
    cache_key = get_story_cache_key(story_data)
    cache_path = get_cache_paths(project_root, cache_key, "captions")
    
    if cache_exists(cache_path):
        print(f"🎯 Using cached captions file...")
        if copy_from_cache(cache_path, srt_path):
            print(f"✅ Cached captions copied to {srt_path}")
            return srt_path
        else:
            print("⚠️  Failed to copy from cache, generating new captions...")
    
    # Initialize ElevenLabs client
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY environment variable not set.")
        return None
    
    elevenlabs = ElevenLabs(api_key=api_key)
    
    # Combine title and story for alignment
    full_text = f"{story_data['title']}. {story_data['story']}"
    
    try:
        # Read the audio file
        with open(voice_file_path, 'rb') as audio_file:
            # Use ElevenLabs forced alignment
            print("Running forced alignment with ElevenLabs...")
            alignment_result = elevenlabs.forced_alignment.create(
                file=audio_file,
                text=full_text
            )
        
        # Extract word-level timing information
        words_with_timing = []
        
        
        # Try different possible attribute names for the response
        if hasattr(alignment_result, 'words'):
            words_data = alignment_result.words
        elif hasattr(alignment_result, 'word_alignments'):
            words_data = alignment_result.word_alignments
        else:
            raise AttributeError("Cannot find words data in alignment result")
        
        for word_info in words_data:
            
            
            # Try different possible attribute names
            word_text = None
            start_time = None
            end_time = None
            
            # Try to get word text
            for attr in ['word', 'text', 'token', 'content']:
                if hasattr(word_info, attr):
                    word_text = getattr(word_info, attr)
                    break
            
            # Try to get start time
            for attr in ['start_time_seconds', 'start_time', 'start', 'begin']:
                if hasattr(word_info, attr):
                    start_time = getattr(word_info, attr)
                    break
            
            # Try to get end time
            for attr in ['end_time_seconds', 'end_time', 'end', 'finish']:
                if hasattr(word_info, attr):
                    end_time = getattr(word_info, attr)
                    break
            
            if word_text and start_time is not None and end_time is not None:
                words_with_timing.append({
                    'word': word_text,
                    'start': start_time,
                    'end': end_time
                })
            else:
                print(f"Debug: Missing data - word: {word_text}, start: {start_time}, end: {end_time}")
                print(f"Debug: Available attributes: {[attr for attr in dir(word_info) if not attr.startswith('_')]}")
                break
        
        print(f"Aligned {len(words_with_timing)} words")
        
        # Group words into caption chunks (configurable words per chunk)
        chunks = []
        current_chunk = {'words': [], 'start': None, 'end': None}
        
        for i, word_data in enumerate(words_with_timing):
            if current_chunk['start'] is None:
                current_chunk['start'] = word_data['start']
            
            current_chunk['words'].append(word_data['word'])
            current_chunk['end'] = word_data['end']
            
            # Create chunk when we reach words_per_chunk or at the end
            if len(current_chunk['words']) >= words_per_chunk or i == len(words_with_timing) - 1:
                chunks.append({
                    'text': ' '.join(current_chunk['words']),
                    'start': current_chunk['start'],
                    'end': current_chunk['end']
                })
                current_chunk = {'words': [], 'start': None, 'end': None}
        
        # Generate SRT content
        srt_content = []
        for i, chunk in enumerate(chunks):
            srt_content.append(f"{i + 1}")
            srt_content.append(f"{format_srt_time(chunk['start'])} --> {format_srt_time(chunk['end'])}")
            srt_content.append(chunk['text'])
            srt_content.append("")  # Empty line between entries
        
        # Write SRT file
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_content))
        
        print(f"Captions generated: {srt_path}")
        print(f"Total duration: {chunks[-1]['end']:.2f} seconds")
        print(f"Number of caption chunks: {len(chunks)}")
        
        # Save to cache
        save_to_cache(srt_path, cache_path)
        
        return srt_path
        
    except Exception as e:
        print(f"Error during forced alignment: {e}")
        return None

def main():
    """
    Main function to generate captions from the latest story and voice files.
    """
    # Get the latest story file
    story_file = get_latest_story_file()
    if not story_file:
        print("No story files found in 'stories/' directory.")
        return
    
    # Get the latest voice file
    voice_file = get_latest_voice_file()
    if not voice_file:
        print("No voice files found in 'voices/' directory.")
        return
    
    # Load story data
    try:
        with open(story_file, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
    except Exception as e:
        print(f"Error reading story file: {e}")
        return
    
    # Generate captions with different chunk sizes
    # For TikTok/Instagram Reels, 1-2 words per chunk works well for engagement
    # For YouTube/longer content, 3-4 words per chunk is more readable
    
    words_per_chunk = 2  # Change this: 1=single word, 2=minimal, 3-4=balanced, 5-8=more text
    print(f"Generating captions with {words_per_chunk} words per chunk...")
    
    captions_path = generate_captions(story_data, voice_file, words_per_chunk=words_per_chunk)
    
    if captions_path:
        print(f"Success! Captions saved to: {captions_path}")
    else:
        print("Failed to generate captions.")

if __name__ == "__main__":
    main()
