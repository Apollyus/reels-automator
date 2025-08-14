
# Save Story to Idea Database

This script is responsible for saving a generated story to the idea database. This helps in keeping track of the generated stories and avoiding duplicates.

## Functions

### `get_latest_story_file()`

This function finds the most recently created story file in the `stories/` directory.

#### Returns

- `str`: The path to the latest story file.
- `None`: If the `stories/` directory does not exist or is empty.

### `save_story_to_database(story_data)`

This function appends a story to the `ideas/ideas.json` file. It also adds a timestamp and an MD5 hash of the story to the data before saving it. The hash can be used for duplicate detection.

This function also saves the title of the story to `ideas/idea_titles.json`.

#### Parameters

- `story_data` (dict): The story to be saved.

## Usage

To run this script, execute the following command in your terminal:

```bash
python src/save_story_to_database.py
```

This will take the latest story from the `stories/` directory and save it to the `ideas/ideas.json` file.
