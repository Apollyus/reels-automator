
# Generate Voiceover

This script is responsible for generating a voiceover from a story using the ElevenLabs API.

## Dependencies

This script requires the `elevenlabs` and `python-dotenv` Python libraries.

- **elevenlabs**: You can install this library using pip:
  ```bash
  pip install elevenlabs
  ```
- **python-dotenv**: You can install this library using pip:
    ```bash
    pip install python-dotenv
    ```

The script imports the ElevenLabs client specifically from `elevenlabs.client`.

## API Key

To use this script, you need an ElevenLabs API key. You can get one from the [ElevenLabs website](https://elevenlabs.io/). You need to create a `.env` file in the root of the project and add the following line to it, replacing `your_api_key` with your actual API key:

```
ELEVENLABS_API_KEY="your_api_key"
```

## Functions

### `get_latest_story_file()`

This function finds the most recently created story file in the `stories/` directory.

#### Returns

- `str`: The path to the latest story file.
- `None`: If the `stories/` directory does not exist or is empty.

### `generate_voiceover(story_data)`

This function takes a story and generates a voiceover from it using the ElevenLabs API. The voiceover is saved as an MP3 file in the `voices/` directory.

#### Parameters

- `story_data` (dict): The story dictionary containing at least a "story" field with the text to be converted to speech.

#### Implementation Details

- Uses voice ID `"JBFqnCBsd6RMkjVDRZzb"` and model `"eleven_multilingual_v2"`
- Extracts the text from `story_data["story"]` field specifically
- Creates the `voices/` directory if it doesn't exist
- Generates filename using current timestamp (e.g., `1678886400.mp3`)
- Includes error handling for API failures
- Prints success/error messages to console

## Usage

To run this script, execute the following command in your terminal:

```bash
venv\Scripts\activate
python src/generate_voiceover.py
```

This will take the latest story from the `stories/` directory and generate a voiceover from it. The voiceover will be saved as an MP3 file in the `voices/` directory. The filename will be a timestamp, e.g., `1678886400.mp3`.
