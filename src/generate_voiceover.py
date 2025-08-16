
import os
import json
import os
import json
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import time

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
    Generates voiceovers from a story using the ElevenLabs API.
    Creates separate files for title, story, and combined audio.

    Args:
        story_data (dict): The story to generate voiceovers for.
    
    Returns:
        dict: Paths to generated audio files or None if error.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY environment variable not set.")
        return None
    
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    voices_dir = os.path.join(project_root, "voices")
    if not os.path.exists(voices_dir):
        os.makedirs(voices_dir)

    timestamp = int(time.time())
    
    # Prepare file paths
    title_path = os.path.join(voices_dir, f"{timestamp}_title.mp3")
    story_path = os.path.join(voices_dir, f"{timestamp}_story.mp3")
    combined_path = os.path.join(voices_dir, f"{timestamp}.mp3")
    
    results = {}

    try:
        # Generate title voiceover
        print("Generating title voiceover...")
        title_audio = elevenlabs.text_to_speech.convert(
            text=story_data["title"],
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
        )
        with open(title_path, "wb") as f:
            for chunk in title_audio:
                f.write(chunk)
        print(f"Title voiceover saved to {title_path}")
        results['title'] = title_path
        
        # Generate story voiceover
        print("Generating story voiceover...")
        story_audio = elevenlabs.text_to_speech.convert(
            text=story_data["story"],
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
        )
        with open(story_path, "wb") as f:
            for chunk in story_audio:
                f.write(chunk)
        print(f"Story voiceover saved to {story_path}")
        results['story'] = story_path
        
        # Generate combined voiceover (title + story)
        print("Generating combined voiceover...")
        combined_text = f"{story_data['title']}. {story_data['story']}"
        combined_audio = elevenlabs.text_to_speech.convert(
            text=combined_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
        )
        with open(combined_path, "wb") as f:
            for chunk in combined_audio:
                f.write(chunk)
        print(f"Combined voiceover saved to {combined_path}")
        results['combined'] = combined_path
        
        return results
        
    except Exception as e:
        print(f"Error generating voiceover: {e}")
        return None

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
