# Generate Captions

This script is responsible for generating timed captions (subtitles) for the voiceover audio in SRT format using ElevenLabs forced alignment.

## Main Function: `generate_captions(story_data, voice_file_path, words_per_chunk=4)`

This is the core function that creates precise timed captions by using ElevenLabs forced alignment API to get exact word-level timing.

### Parameters

- `story_data` (dict): The story data containing title and story text
- `voice_file_path` (str): Path to the MP3 voiceover file
- `words_per_chunk` (int): Number of words to display per caption (default: 4)

### Word Chunk Options

- **1 word**: Single word display for maximum engagement (TikTok style)
- **2 words**: Minimal text, easy to read on mobile screens
- **3-4 words**: Balanced readability (recommended for most content)
- **5-8 words**: More text per caption, less frequent changes

### Returns

- `str`: Path to the generated SRT caption file, or `None` if generation failed

### Process

1. **Forced Alignment**: Uses ElevenLabs API to analyze the audio and text, getting precise word-level timestamps
2. **Word Grouping**: Groups words into configurable chunks (1-8 words) based on the `words_per_chunk` parameter
3. **Timing Extraction**: Uses exact start/end times from the alignment for each chunk
4. **SRT Generation**: Creates properly formatted SRT subtitle file with precise timing

## Platform Recommendations

### TikTok/Instagram Reels (`words_per_chunk=1-2`)
- **1 word**: Maximum engagement, dramatic effect
- **2 words**: Minimal text, easy mobile reading

### YouTube Shorts (`words_per_chunk=2-3`)
- **2-3 words**: Good balance of engagement and readability

### Longer Content (`words_per_chunk=4-6`)
- **4-6 words**: More efficient, less distracting for longer videos

## Helper Functions

### `get_latest_story_file()`

Finds the most recently created story JSON file in the `stories/` directory.

### `get_latest_voice_file()`

Finds the most recently created voice MP3 file in the `voices/` directory.

### `format_srt_time(seconds)`

Converts seconds to SRT time format (HH:MM:SS,mmm).

- **Parameters**: `seconds` (float): Time in seconds
- **Returns**: Formatted time string

## Output Format

The script generates an SRT (SubRip Subtitle) file with precise timing. The format varies based on `words_per_chunk`:

### Single Word (`words_per_chunk=1`)
```
1
00:00:00,000 --> 00:00:00,340
My

2
00:00:00,340 --> 00:00:00,680
girlfriend

3
00:00:00,680 --> 00:00:01,020
is
```

### Minimal Text (`words_per_chunk=2`)
```
1
00:00:00,000 --> 00:00:00,680
My girlfriend

2
00:00:00,680 --> 00:00:01,200
is a

3
00:00:01,200 --> 00:00:01,850
ghost, but
```

### Balanced (`words_per_chunk=4`)
```
1
00:00:00,000 --> 00:00:01,850
My girlfriend is a

2
00:00:01,850 --> 00:00:03,200
ghost, but I'm the

3
00:00:03,200 --> 00:00:04,750
only one who can
```

## Usage

To run this script independently with default settings (4 words per chunk):

```bash
python src/generate_captions.py
```

To customize word chunking, modify the `words_per_chunk` variable in the `main()` function:

```python
# For TikTok-style single word captions
words_per_chunk = 1

# For minimal text (recommended for mobile)
words_per_chunk = 2

# For balanced readability
words_per_chunk = 4

# For more text per caption
words_per_chunk = 6
```

This will:
1. Find the latest story JSON file
2. Find the latest voice MP3 file  
3. Use ElevenLabs forced alignment for precise timing
4. Generate accurately timed SRT file with specified word chunking in `captions/` directory

## Dependencies

- `elevenlabs`: For forced alignment API access
- `python-dotenv`: For environment variable management
- `json`: For reading story data
- `os`: For file system operations

## Environment Variables

- `ELEVENLABS_API_KEY`: Required for accessing the forced alignment API

## Output Location

Caption files are saved as: `captions/{timestamp}.srt`

Where `{timestamp}` matches the timestamp from the corresponding voice file.

## Advantages of Forced Alignment

- **Precise Timing**: Word-level accuracy instead of estimated timing
- **Natural Flow**: Respects actual speech patterns and pauses
- **Better Synchronization**: Perfect alignment with audio content
- **Professional Quality**: Suitable for commercial video production
- **Flexible Display**: Configurable word chunking for different platforms and engagement styles
- **Platform Optimization**: Easily adjust caption density for TikTok, YouTube, Instagram, etc.
