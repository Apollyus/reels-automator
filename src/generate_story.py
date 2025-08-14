
import json
import time
import os

def generate_story():
    """
    Generates a story in the style of a Reddit post.

    This is currently a placeholder and returns a hardcoded story.
    In the future, this will be replaced with a call to an LLM API.

    Returns:
        dict: A dictionary containing the story details.
    """
    return {
        "title": "My girlfriend is a ghost, but I'm the only one who can see her.",
        "story": "My girlfriend, Clara, died in a car accident a year ago. I was devastated. We had been together for five years, and I thought we were going to get married. A few weeks after she died, I started seeing her. At first, I thought I was going crazy. But then she started talking to me. She told me that she was still with me, and that she would always be with me. I was so happy. I had my Clara back. We've been together for a year now, and it's been the best year of my life. I know it's not the same as having her here in person, but it's close enough. I love her so much, and I'm so grateful to have her back in my life.",
        "subreddit": "r/nosleep",
        "username": "u/hauntedlover",
        "upvotes": 12345
    }

if __name__ == "__main__":
    story_data = generate_story()
    
    # Create the stories directory if it doesn't exist
    if not os.path.exists("stories"):
        os.makedirs("stories")

    # Save the story to a JSON file
    timestamp = int(time.time())
    file_path = os.path.join("stories", f"{timestamp}.json")
    with open(file_path, "w") as f:
        json.dump(story_data, f, indent=4)

    print(f"Story saved to {file_path}")
