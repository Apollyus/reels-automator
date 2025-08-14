
import json
import os
import hashlib
import time

def get_latest_story_file():
    """
    Gets the path to the latest story file in the 'stories' directory.

    Returns:
        str: The path to the latest story file, or None if the directory is empty.
    """
    stories_dir = "stories"
    if not os.path.exists(stories_dir):
        return None

    files = [os.path.join(stories_dir, f) for f in os.listdir(stories_dir) if f.endswith(".json")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def save_story_to_database(story_data):
    """
    Saves a story to the idea database.

    Args:
        story_data (dict): The story to save.
    """
    ideas_dir = "ideas"
    if not os.path.exists(ideas_dir):
        os.makedirs(ideas_dir)

    database_path = os.path.join(ideas_dir, "ideas.json")

    database = []
    if os.path.exists(database_path):
        with open(database_path, "r") as f:
            database = json.load(f)

    # Add timestamp and hash for duplicate detection
    story_data["timestamp"] = int(time.time())
    story_data["hash"] = hashlib.md5(json.dumps(story_data, sort_keys=True).encode()).hexdigest()

    database.append(story_data)

    with open(database_path, "w") as f:
        json.dump(database, f, indent=4)

    print(f"Story saved to {database_path}")

    # Save the title to a separate file
    titles_path = os.path.join(ideas_dir, "idea_titles.json")
    titles = []
    if os.path.exists(titles_path):
        with open(titles_path, "r") as f:
            titles = json.load(f)

    titles.append(story_data["title"])

    with open(titles_path, "w") as f:
        json.dump(titles, f, indent=4)

    print(f"Story title saved to {titles_path}")

if __name__ == "__main__":
    latest_story_file = get_latest_story_file()
    if latest_story_file:
        with open(latest_story_file, "r") as f:
            story_data = json.load(f)
        save_story_to_database(story_data)
    else:
        print("No stories found to save.")
