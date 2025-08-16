# Installation and Setup Guide

This guide will help you set up the Minecraft Reddit Story Reels Generator on your system.

## Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg:**
   - Windows: Download from https://ffmpeg.org/download.html or use `winget install FFmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

3. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

5. **Add background videos:**
   Place your Minecraft gameplay videos in the `background/` directory (MP4, AVI, MOV, or MKV format)

6. **Run the generator:**
   ```bash
   python main.py --count 1 --background your_background_video.mp4
   ```

## Detailed Setup Instructions

### 1. Python Environment Setup

#### Option A: Using Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv reels-env

# Activate virtual environment
# Windows:
reels-env\Scripts\activate
# macOS/Linux:
source reels-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using Conda
```bash
# Create conda environment
conda create -n reels-automator python=3.9

# Activate environment
conda activate reels-automator

# Install dependencies
pip install -r requirements.txt
```

### 2. ElevenLabs API Setup

1. **Create an ElevenLabs account:**
   - Visit https://elevenlabs.io/
   - Sign up for an account
   - Get your API key from the profile settings

2. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   ELEVENLABS_API_KEY=your_actual_api_key_here
   ```

3. **Verify API access:**
   Test your setup by running:
   ```bash
   python -c "from elevenlabs import client; print('ElevenLabs API connection successful!')"
   ```

### 3. FFmpeg Installation

#### Windows
```bash
# Option 1: Using winget (Windows 10/11)
winget install FFmpeg

# Option 2: Manual installation
# 1. Download from https://ffmpeg.org/download.html
# 2. Extract to C:\ffmpeg
# 3. Add C:\ffmpeg\bin to your PATH environment variable
```

#### macOS
```bash
# Using Homebrew
brew install ffmpeg

# Using MacPorts
sudo port install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Linux (CentOS/RHEL/Fedora)
```bash
# Enable EPEL repository first (CentOS/RHEL)
sudo yum install epel-release

# Install FFmpeg
sudo yum install ffmpeg

# For Fedora:
sudo dnf install ffmpeg
```

#### Verify FFmpeg Installation
```bash
ffmpeg -version
```

### 4. Playwright Browser Setup

After installing the Python package, install browser engines:

```bash
# Install Chromium (required for HTML to image conversion)
playwright install chromium

# Optional: Install all browsers
playwright install
```

### 5. Directory Structure Setup

The script will automatically create required directories, but you can set them up manually:

```bash
mkdir -p background stories voices images captions exports ideas
```

### 6. Background Videos

Add your Minecraft gameplay videos to the `background/` directory:

- **Supported formats:** MP4, AVI, MOV, MKV
- **Recommended specs:**
  - Resolution: 1920x1080 or higher
  - Duration: 60+ seconds (will be looped if needed)
  - Frame rate: 30fps or 60fps
  - Good quality gameplay footage

**Example background videos to add:**
- `minecraft_parkour.mp4`
- `minecraft_building.mp4`
- `minecraft_survival.mp4`
- `minecraft_pvp.mp4`

### 7. Testing Your Setup

Run a test generation to verify everything works:

```bash
python main.py --count 1 --background your_background_video.mp4
```

Expected output structure:
```
stories/1234567890.json           # Story data
voices/1234567890_title.mp3       # Title audio
voices/1234567890_story.mp3       # Story audio
voices/1234567890.mp3             # Combined audio
images/1234567890_title.png       # Reddit post image
captions/1234567890.srt           # Subtitles
exports/final_1234567890.mp4      # Final video
```

## Troubleshooting

### Common Issues

1. **"elevenlabs module not found"**
   ```bash
   pip install elevenlabs
   ```

2. **"FFmpeg not found"**
   - Ensure FFmpeg is installed and in your PATH
   - Test with: `ffmpeg -version`

3. **"Playwright browser not found"**
   ```bash
   playwright install chromium
   ```

4. **"ElevenLabs API key invalid"**
   - Check your `.env` file
   - Verify API key on ElevenLabs website
   - Ensure no extra spaces in the key

5. **"Background video not found"**
   - Verify the file exists in the `background/` directory
   - Check file extension is supported (MP4, AVI, MOV, MKV)

### Performance Optimization

1. **For faster generation:**
   - Use SSD storage
   - Ensure good internet connection for ElevenLabs API
   - Use shorter background videos (reduces processing time)

2. **For better quality:**
   - Use high-quality background videos (1920x1080+)
   - Choose appropriate `--words-per-chunk` setting for your audience

### System Requirements

- **Python:** 3.7 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 1GB free space per video generated
- **Internet:** Required for ElevenLabs API calls
- **CPU:** Multi-core recommended for faster processing

## Advanced Configuration

### Custom Voice Settings

Modify `src/generate_voiceover.py` to customize:
- Voice model (different ElevenLabs voices)
- Speech speed and stability
- Emotional emphasis

### Custom Video Format

Modify `src/compose_video.py` to change:
- Video resolution (currently 1080x1920)
- Video codec settings
- Caption styling

### Story Generation Enhancement

Replace the placeholder story generation in `src/generate_story.py` with:
- OpenAI GPT integration
- Anthropic Claude integration
- Custom story templates

## Getting Help

If you encounter issues:

1. Check this installation guide
2. Review error messages carefully
3. Verify all dependencies are installed
4. Test individual components
5. Check the project documentation in `docs/`

## Next Steps

Once everything is working:
1. Generate your first batch of videos
2. Customize story templates
3. Add more background videos
4. Experiment with different voice settings
5. Set up automated scheduling for regular content creation
