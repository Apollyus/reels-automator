
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

- `story_data` (dict): The story to be used for the voiceover.

## Usage

To run this script, execute the following command in your terminal:

```bash
venv\Scripts\activate
python src/generate_voiceover.py
```

This will take the latest story from the `stories/` directory and generate a voiceover from it. The voiceover will be saved as an MP3 file in the `voices/` directory. The filename will be a timestamp, e.g., `1678886400.mp3`.
