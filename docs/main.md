# Main Pipeline Script

This is the main orchestrator script that runs the complete Minecraft Reddit Story Reels generation pipeline.

## Usage

```bash
python main.py --count <number_of_videos> --background <background_video_filename>
```

### Required Arguments

- `--count`: Number of videos to generate in one run (integer, minimum 1)
- `--background`: Filename of the background video from the 'background/' directory

### Optional Arguments

- `--words-per-chunk`: Number of words per caption chunk (1-8, default: 2)
  - `1`: Single word captions (maximum engagement)
  - `2`: Minimal text (recommended for mobile)
  - `3-4`: Balanced readability
  - `5-8`: More text per caption

## Examples

```bash
# Generate 1 video with specific background
python main.py --count 1 --background minecraft_parkour.mp4

# Generate 5 videos with minimal captions
python main.py --count 5 --background parkour_loop.mp4 --words-per-chunk 2

# Generate 3 videos with balanced captions
python main.py --count 3 --background gameplay.mp4 --words-per-chunk 4
```

## Complete Pipeline Execution

The script executes all 6 steps of the pipeline automatically:

### Step 0: Check Idea Database
- Validates that similar story ideas don't already exist
- Prevents duplicate content generation
- Uses MD5 hash comparison of story titles

### Step 1: Generate Story
- Creates a new Reddit-style story with title, content, subreddit, username, upvotes
- Currently uses placeholder data (will be enhanced with LLM integration)

### Step 2: Save Story to Database
- Saves story JSON file with timestamp
- Appends story to ideas database for future duplicate checking
- Includes hash for efficient comparison

### Step 3: Render Opening Reddit Post Image
- Generates PNG image of the Reddit post using HTML/CSS template
- Creates realistic-looking Reddit post visualization

### Step 4: Generate Voiceover
- Creates three audio files: title-only, story-only, and combined
- Uses ElevenLabs API for high-quality text-to-speech
- Enables sophisticated video composition with separate audio tracks

### Step 5: Generate Timed Captions
- Uses ElevenLabs forced alignment for precise word-level timing
- Creates SRT subtitle file with configurable word chunking
- Ensures perfect synchronization with voiceover

### Step 6: Compose Final Video
- Combines all elements using FFmpeg
- Creates vertical 1080x1920 MP4 optimized for social media
- Features dynamic timing with title audio during opening image

## Output Structure

Each video generation creates:

```
stories/
  └── {timestamp}.json           # Story data

voices/
  ├── {timestamp}_title.mp3      # Title voiceover
  ├── {timestamp}_story.mp3      # Story voiceover
  └── {timestamp}.mp3            # Combined audio

images/
  └── {timestamp}_title.png      # Reddit post image

captions/
  └── {timestamp}.srt            # Subtitle file

exports/
  └── final_{timestamp}.mp4      # Final video
```

## Prerequisites

### Required Files
- Background videos in `background/` directory (MP4, AVI, MOV, MKV)
- `.env` file with `ELEVENLABS_API_KEY`

### Required Software
- Python 3.7+
- FFmpeg (for video composition)
- All Python dependencies (see requirements.txt)

### Directory Structure
The script automatically creates required directories:
- `stories/` - Story JSON files
- `voices/` - Audio files
- `images/` - Reddit post images
- `captions/` - Subtitle files
- `exports/` - Final videos
- `ideas/` - Ideas database

## Error Handling

The script includes comprehensive error handling:

- **Dependency Validation**: Checks for required modules and files
- **Step-by-Step Validation**: Each pipeline step is validated before proceeding
- **Background Video Validation**: Ensures specified video exists
- **Graceful Failures**: Detailed error messages with suggested solutions
- **Progress Tracking**: Shows timing and success/failure for each step

## Performance Metrics

The script tracks and reports:
- Execution time for each pipeline step
- Total pipeline execution time
- Average time per video (for multiple videos)
- Success/failure rates

## Example Output

```
🚀 Minecraft Reddit Story Reels Generator
==================================================
📊 Generating 2 video(s)
🎮 Background video: minecraft_parkour.mp4
📝 Words per caption: 2

============================================================
🎬 GENERATING VIDEO 1/2
============================================================

🔄 Starting: Step 1: Generate Story
✅ Completed: Step 1: Generate Story (0.05s)
📖 Generated story: 'My girlfriend is a ghost, but I'm the only one who can see her.'

🔄 Starting: Step 4: Generate Voiceover
✅ Completed: Step 4: Generate Voiceover (8.34s)
🔊 Generated audio files:
   Title: 1755184388_title.mp3
   Story: 1755184388_story.mp3
   Combined: 1755184388.mp3

🎉 SUCCESS! Video 1/2 completed!
📁 Output: exports/final_1755184388.mp4
⏱️  Total time: 45.67 seconds
🎬 Video duration: 23.45 seconds
```

## Social Media Optimization

Generated videos are optimized for:
- **TikTok**: 1080x1920, MP4, H.264
- **Instagram Reels**: 1080x1920, MP4, H.264  
- **YouTube Shorts**: 1080x1920, MP4, H.264
- **Facebook Reels**: 1080x1920, MP4, H.264

All outputs are ready for direct upload without additional processing.
