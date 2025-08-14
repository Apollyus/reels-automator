
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
    Generates a voiceover from a story using the ElevenLabs API.

    Args:
        story_data (dict): The story to generate a voiceover for.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY environment variable not set.")
        return
    
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    voices_dir = os.path.join(project_root, "voices")
    if not os.path.exists(voices_dir):
        os.makedirs(voices_dir)

    timestamp = int(time.time())
    output_path = os.path.join(voices_dir, f"{timestamp}.mp3")

    try:
        audio = elevenlabs.text_to_speech.convert(
            text=story_data["story"],
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
        )
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print(f"Voiceover saved to {output_path}")
    except Exception as e:
        print(f"Error generating voiceover: {e}")

if __name__ == "__main__":
    latest_story_file = get_latest_story_file()
    if latest_story_file:
        with open(latest_story_file, "r") as f:
            story_data = json.load(f)
        generate_voiceover(story_data)
    else:
        print("No stories found to generate a voiceover for.")
