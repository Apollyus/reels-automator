# Compose Final Video

This script is responsible for composing the final vertical video by combining all generated assets using FFmpeg.

## Main Function: `compose_final_video(background_video_path, opening_image_path, title_voice_path, story_voice_path, captions_path, output_path, opening_duration=3.0)`

This is the core function that uses FFmpeg to create the final video with separate title and story audio for enhanced engagement.

### Parameters

- `background_video_path` (str): Path to the Minecraft parkour background video
- `opening_image_path` (str): Path to the Reddit post opening image (PNG)
- `title_voice_path` (str): Path to the title voiceover audio file (MP3)
- `story_voice_path` (str): Path to the story voiceover audio file (MP3)
- `captions_path` (str): Path to the subtitle file (SRT)
- `output_path` (str): Path where the final video will be saved
- `opening_duration` (float): Minimum duration for opening image (default: 3.0 seconds)

### Returns

- `bool`: True if video composition was successful, False otherwise

### Enhanced Audio Experience

The function creates a sophisticated audio experience:
1. **Title Audio**: Plays during the Reddit post opening image
2. **Story Audio**: Plays during the Minecraft parkour background
3. **Seamless Transition**: Audio flows naturally from title to story
4. **Dynamic Timing**: Opening duration adjusts to title length automatically

### Process

1. **Duration Analysis**: Uses FFprobe to get exact duration of both title and story audio
2. **Smart Timing**: Automatically adjusts opening image duration to match title length
3. **Format Conversion**: Ensures all inputs are in the correct format for FFmpeg
4. **Video Scaling**: Scales all video content to vertical 1080x1920 format
5. **Audio Sequencing**: Concatenates title and story audio for seamless playback
6. **Layering**: Combines opening image + background video + sequential audio + captions
7. **Encoding**: Outputs high-quality MP4 suitable for social media platforms

## Video Composition Structure

### Enhanced Timeline
```
0s ──── Title Duration ──────────────── Total Duration
│       │                              │
│ Opening Image    │   Background Video │
│ + Title Audio    │   + Story Audio   │
│                  │   + Captions      │
```

### Audio Flow
1. **Title Phase**: Reddit post title spoken while image is displayed
2. **Story Phase**: Main story narrated during Minecraft parkour footage
3. **Captions**: Precisely timed subtitles throughout entire video

### Visual Layers (bottom to top)
1. **Background Video**: Minecraft parkour footage (scaled to 1080x1920)
2. **Opening Image**: Reddit post (shown for first 3 seconds)
3. **Captions**: Precisely timed subtitles with styling

## Helper Functions

### `get_latest_story_file()`
Finds the most recently created story JSON file.

### `get_latest_voice_file()`
Finds the most recently created voice MP3 file.

### `get_latest_image_file()`
Finds the most recently created image PNG file.

### `get_latest_caption_file()`
Finds the most recently created caption SRT file.

### `get_audio_duration(audio_path)`
Uses FFprobe to get exact audio duration in seconds.

## Caption Styling

The script applies professional subtitle styling:
- **Font Size**: 24pt
- **Color**: White with black outline
- **Position**: Bottom center with margin
- **Outline**: 2px black border for readability
- **Shadow**: Subtle drop shadow

## Output Specifications

- **Resolution**: 1080x1920 (vertical/portrait)
- **Video Codec**: H.264 (libx264)
- **Audio Codec**: AAC 128kbps
- **Format**: MP4
- **Quality**: CRF 23 (high quality, suitable for social media)

## Usage

### Automatic Mode (uses latest files)
```bash
python src/compose_video.py
```

### With Specific Background Video
```bash
python src/compose_video.py minecraft_parkour_1.mp4
```

This will:
1. Find all latest generated assets (story, voice, image, captions)
2. Use specified or first available background video
3. Compose final video with professional quality
4. Save to `exports/final_{timestamp}.mp4`

## Dependencies

- **FFmpeg**: Required for video processing and composition
- **FFprobe**: Required for audio duration analysis (included with FFmpeg)

## File Requirements

Before running, ensure these files exist:
- Latest story JSON in `stories/`
- Latest title voice MP3 in `voices/` (ending with `_title.mp3`)
- Latest story voice MP3 in `voices/` (ending with `_story.mp3`)
- Latest image PNG in `images/`
- Latest caption SRT in `captions/`
- Background video in `background/`

**Note**: Run `generate_voiceover.py` to create the separate title and story audio files required for enhanced video composition.

## Output Location

Final videos are saved as: `exports/final_{timestamp}.mp4`

## Platform Compatibility

The output video is optimized for:
- **TikTok**: 1080x1920, MP4, H.264
- **Instagram Reels**: 1080x1920, MP4, H.264
- **YouTube Shorts**: 1080x1920, MP4, H.264
- **Facebook Reels**: 1080x1920, MP4, H.264

All major social media platforms support this format natively.
