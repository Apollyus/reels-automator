import os
import json
import subprocess
import time
from pathlib import Path

def get_latest_story_file():
    """
    Gets the path to the latest story file in the 'stories' directory.

    Returns:
        str: The path to the latest story file, or None if the directory is empty.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    stories_dir = os.path.join(project_root, "stories")
    
    if not os.path.exists(stories_dir):
        return None

    files = [os.path.join(stories_dir, f) for f in os.listdir(stories_dir) if f.endswith(".json")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def get_latest_voice_file():
    """
    Gets the path to the latest voice file in the 'voices' directory.

    Returns:
        str: The path to the latest voice file, or None if the directory is empty.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    voices_dir = os.path.join(project_root, "voices")
    
    if not os.path.exists(voices_dir):
        return None

    files = [os.path.join(voices_dir, f) for f in os.listdir(voices_dir) if f.endswith(".mp3")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def get_latest_title_voice_file():
    """
    Gets the path to the latest title voice file in the 'voices' directory.

    Returns:
        str: The path to the latest title voice file, or None if not found.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    voices_dir = os.path.join(project_root, "voices")
    
    if not os.path.exists(voices_dir):
        return None

    files = [os.path.join(voices_dir, f) for f in os.listdir(voices_dir) if f.endswith("_title.mp3")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def get_latest_story_voice_file():
    """
    Gets the path to the latest story voice file in the 'voices' directory.

    Returns:
        str: The path to the latest story voice file, or None if not found.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    voices_dir = os.path.join(project_root, "voices")
    
    if not os.path.exists(voices_dir):
        return None

    files = [os.path.join(voices_dir, f) for f in os.listdir(voices_dir) if f.endswith("_story.mp3")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def get_latest_image_file():
    """
    Gets the path to the latest image file in the 'images' directory.

    Returns:
        str: The path to the latest image file, or None if the directory is empty.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    images_dir = os.path.join(project_root, "images")
    
    if not os.path.exists(images_dir):
        return None

    files = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.endswith(".png")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def get_latest_caption_file():
    """
    Gets the path to the latest caption file in the 'captions' directory.

    Returns:
        str: The path to the latest caption file, or None if the directory is empty.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    captions_dir = os.path.join(project_root, "captions")
    
    if not os.path.exists(captions_dir):
        return None

    files = [os.path.join(captions_dir, f) for f in os.listdir(captions_dir) if f.endswith(".srt")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def get_audio_duration(audio_path):
    """
    Gets the duration of an audio file using FFprobe.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        float: Duration in seconds, or None if error.
    """
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "csv=p=0", audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return None

def compose_final_video(background_video_path, opening_image_path, title_voice_path, story_voice_path, captions_path, output_path, opening_duration=3.0):
    """
    Composes the final video using FFmpeg with separate title and story audio.

    Args:
        background_video_path (str): Path to the background Minecraft video.
        opening_image_path (str): Path to the opening Reddit post image.
        title_voice_path (str): Path to the title voiceover audio.
        story_voice_path (str): Path to the story voiceover audio.
        captions_path (str): Path to the SRT caption file.
        output_path (str): Path for the output video.
        opening_duration (float): Duration to show opening image (default: 3.0 seconds).

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Get audio durations
        title_duration = get_audio_duration(title_voice_path)
        story_duration = get_audio_duration(story_voice_path)
        
        if not title_duration or not story_duration:
            print("Failed to get audio durations")
            return False
        
        # Calculate timing
        total_duration = title_duration + story_duration
        # Use title duration for opening image, but ensure minimum of opening_duration
        actual_opening_duration = max(title_duration, opening_duration)
        
        print(f"Title duration: {title_duration:.2f} seconds")
        print(f"Story duration: {story_duration:.2f} seconds")
        print(f"Total duration: {total_duration:.2f} seconds")
        print(f"Opening image duration: {actual_opening_duration:.2f} seconds")
        
        # Convert paths to use forward slashes for FFmpeg
        background_video_path = background_video_path.replace('\\', '/')
        opening_image_path = opening_image_path.replace('\\', '/')
        title_voice_path = title_voice_path.replace('\\', '/')
        story_voice_path = story_voice_path.replace('\\', '/')
        captions_path = captions_path.replace('\\', '/')
        output_path = output_path.replace('\\', '/')
        
        # Complex FFmpeg command to create the final video
        cmd = [
            "ffmpeg", "-y",  # Overwrite output file
            
            # Input 1: Opening image (convert to video with title duration)
            "-loop", "1", "-i", opening_image_path, "-t", str(actual_opening_duration),
            
            # Input 2: Background video
            "-i", background_video_path,
            
            # Input 3: Title audio
            "-i", title_voice_path,
            
            # Input 4: Story audio
            "-i", story_voice_path,
            
            # Filter complex to combine everything
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[opening];"
            f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[bg];"
            f"[opening][bg]concat=n=2:v=1:a=0[video];"
            f"[2:a][3:a]concat=n=2:v=0:a=1[audio];"
            f"[video]subtitles='{captions_path}':force_style='Fontsize=24,PrimaryColour=&H00ffffff,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=100'[final_video]",
            
            # Map the final video and audio
            "-map", "[final_video]", "-map", "[audio]",
            
            # Video settings for social media (vertical format)
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-pix_fmt", "yuv420p",
            
            # Audio settings
            "-c:a", "aac", "-b:a", "128k",
            
            # Duration (match total audio duration)
            "-t", str(total_duration),
            
            # Output
            output_path
        ]
        
        print("Running FFmpeg command...")
        print(" ".join(cmd))
        
        # Run FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("Video composition completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        print(f"FFmpeg stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error during video composition: {e}")
        return False

def main(background_video_filename=None):
    """
    Main function to compose the final video from the latest generated assets.

    Args:
        background_video_filename (str): Optional specific background video filename.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Get all required files
    story_file = get_latest_story_file()
    title_voice_file = get_latest_title_voice_file()
    story_voice_file = get_latest_story_voice_file()
    image_file = get_latest_image_file()
    caption_file = get_latest_caption_file()
    
    # Check if all files exist
    missing_files = []
    if not story_file:
        missing_files.append("story JSON")
    if not title_voice_file:
        missing_files.append("title voice MP3")
    if not story_voice_file:
        missing_files.append("story voice MP3")
    if not image_file:
        missing_files.append("image PNG")
    if not caption_file:
        missing_files.append("caption SRT")
    
    if missing_files:
        print(f"Missing required files: {', '.join(missing_files)}")
        print("Please ensure all pipeline steps have been completed.")
        print("Note: Run generate_voiceover.py to create separate title and story audio files.")
        return
    
    # Get background video
    background_dir = os.path.join(project_root, "background")
    if background_video_filename:
        background_video_path = os.path.join(background_dir, background_video_filename)
        if not os.path.exists(background_video_path):
            print(f"Specified background video not found: {background_video_filename}")
            return
    else:
        # Get any video from background directory
        if not os.path.exists(background_dir):
            print("Background directory not found. Please add Minecraft parkour videos to 'background/' directory.")
            return
        
        video_files = [f for f in os.listdir(background_dir) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        if not video_files:
            print("No video files found in 'background/' directory.")
            return
        
        background_video_path = os.path.join(background_dir, video_files[0])
        print(f"Using background video: {video_files[0]}")
    
    # Create output directory
    exports_dir = os.path.join(project_root, "exports")
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    
    # Generate output filename
    timestamp = int(time.time())
    output_filename = f"final_{timestamp}.mp4"
    output_path = os.path.join(exports_dir, output_filename)
    
    print("Composing final video with separate title and story audio...")
    print(f"Story: {os.path.basename(story_file)}")
    print(f"Title Voice: {os.path.basename(title_voice_file)}")
    print(f"Story Voice: {os.path.basename(story_voice_file)}")
    print(f"Image: {os.path.basename(image_file)}")
    print(f"Captions: {os.path.basename(caption_file)}")
    print(f"Background: {os.path.basename(background_video_path)}")
    print(f"Output: {output_filename}")
    
    # Compose the video
    success = compose_final_video(
        background_video_path=background_video_path,
        opening_image_path=image_file,
        title_voice_path=title_voice_file,
        story_voice_path=story_voice_file,
        captions_path=caption_file,
        output_path=output_path
    )
    
    if success:
        print(f"🎉 Success! Final video saved to: {output_path}")
        print(f"Video includes title voiceover during opening image!")
        print(f"Video is ready for upload to TikTok, Instagram Reels, YouTube Shorts!")
    else:
        print("❌ Failed to compose final video.")

if __name__ == "__main__":
    import sys
    
    # Allow passing background video filename as argument
    background_video = sys.argv[1] if len(sys.argv) > 1 else None
    main(background_video)
