{
  "project_name": "Minecraft Reddit Story Reels Generator",
  "description": "Automated pipeline that generates a fake Reddit post story, renders it visually as an opening frame, creates a voiceover with timed captions, combines it with Minecraft parkour footage, and outputs a vertical video.",
  "cli_usage": "python main.py --count <number_of_videos> --background <background_video_filename>",
  "cli_arguments": {
    "count": {
      "type": "integer",
      "description": "Number of videos to generate in one run."
    },
    "background": {
      "type": "string",
      "description": "Filename of the background video from the 'background/' directory."
    }
  },
  "pipeline": [
    {
      "step": 0,
      "name": "Check Idea Database",
      "input": "Database or JSON of previous story ideas",
      "process": "Before generating a new story, check if a similar idea already exists. If yes, request AI to generate a different one.",
      "output_file": "ideas/ideas.json"
    },
    {
      "step": 1,
      "name": "Generate Story",
      "input": "Topic parameters (theme, style, language)",
      "process": "Call LLM API (e.g., OpenAI, Mistral) with prompt to create short story in Reddit post style.",
      "output_format": {
        "title": "string",
        "story": "string",
        "subreddit": "string",
        "username": "string",
        "upvotes": "integer"
      },
      "output_file": "stories/{timestamp}.json"
    },
    {
      "step": 2,
      "name": "Save Story to Idea Database",
      "input": "Story JSON from step 1",
      "process": "Append the new story idea to the database file (ideas/ideas.json) with timestamp and hash for duplicate detection."
    },
    {
      "step": 3,
      "name": "Render Opening Reddit Post Image",
      "input": "Story JSON from step 1",
      "process": "Inject title, subreddit, username, and upvotes into HTML + CSS Reddit post template, then render to PNG using Puppeteer or Playwright.",
      "output_file": "images/{timestamp}_title.png"
    },
    {
      "step": 4,
      "name": "Generate Voiceover",
      "input": "Story text from step 1",
      "process": "Send text to TTS API (e.g., ElevenLabs, OpenAI TTS) to produce natural-sounding speech.",
      "output_file": "voices/{timestamp}.mp3"
    },
    {
      "step": 5,
      "name": "Generate Timed Captions",
      "input": [
        "Story text from step 1",
        "Voiceover audio duration from step 4"
      ],
      "process": "Split story into chunks of 3–5 words, align each chunk to voiceover timing, export as SRT or ASS subtitle file.",
      "output_file": "captions/{timestamp}.srt"
    },
    {
      "step": 6,
      "name": "Compose Final Video",
      "input": [
        "Background Minecraft parkour video specified in CLI argument",
        "Opening PNG from step 3",
        "Voiceover MP3 from step 4",
        "Timed captions from step 5"
      ],
      "process": "Use FFmpeg to: (1) show opening PNG for first few seconds, (2) switch to background video, (3) overlay captions, (4) sync with audio, and export vertical 1080x1920 MP4.",
      "output_file": "exports/final_{timestamp}.mp4"
    }
  ],
  "directories": {
    "background": "Folder with Minecraft parkour video loops",
    "templates": "HTML and CSS files for Reddit post rendering",
    "voices": "Generated voiceover files",
    "stories": "Generated story JSON files",
    "images": "Rendered PNG post images",
    "exports": "Final videos",
    "ideas": "Database of previously generated ideas",
    "captions": "Generated subtitle files"
  },
  "future_expansion": [
    "Automated upload to TikTok, YouTube Shorts, Instagram Reels, Facebook Reels via API",
    "Local LLM model instead of API",
    "Local TTS model instead of API",
    "Multiple template styles for variety",
    "Web-based dashboard for monitoring, previewing, and editing videos before export",
    "Automatic background video switching for variety"
  ]
}