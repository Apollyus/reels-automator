import os
import json
import subprocess
import time
from pathlib import Path

def find_ffmpeg_path():
    """
    Find FFmpeg/ffprobe executable path on Windows.
    
    Returns:
        tuple: (ffmpeg_path, ffprobe_path) or (None, None) if not found
    """
    # Common Windows locations for FFmpeg
    common_paths = [
        # WinGet installation path
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WinGet', 'Links'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WinGet', 'Packages', 'Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe', 'ffmpeg-7.1.1-full_build', 'bin'),
        # Program Files locations
        r'C:\Program Files\ffmpeg\bin',
        r'C:\Program Files (x86)\ffmpeg\bin',
        # User PATH locations
        r'C:\ffmpeg\bin',
    ]
    
    # First try system PATH
    try:
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
        return 'ffmpeg', 'ffprobe'
    except:
        pass
    
    # Search common installation paths
    for path in common_paths:
        ffmpeg_exe = os.path.join(path, 'ffmpeg.exe')
        ffprobe_exe = os.path.join(path, 'ffprobe.exe')
        if os.path.exists(ffmpeg_exe) and os.path.exists(ffprobe_exe):
            return ffmpeg_exe, ffprobe_exe
    
    return None, None

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
        ffmpeg_path, ffprobe_path = find_ffmpeg_path()
        if not ffprobe_path:
            print("FFprobe not found. Please install FFmpeg.")
            return None
            
        cmd = [
            ffprobe_path, "-v", "quiet", "-show_entries", "format=duration",
            "-of", "csv=p=0", audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return None

def create_story_only_srt(original_srt_path, output_srt_path, start_time):
    """
    Creates a new SRT file containing only subtitles after the specified start time.
    
    Args:
        original_srt_path (str): Path to the original SRT file.
        output_srt_path (str): Path for the new story-only SRT file.
        start_time (float): Time in seconds when story begins.
    """
    try:
        with open(original_srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = content.strip().split('\n\n')
        story_blocks = []
        subtitle_index = 1
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                time_line = lines[1]
                text = lines[2]
                
                if '-->' in time_line:
                    # Parse start time
                    start_time_str = time_line.split('-->')[0].strip()
                    time_parts = start_time_str.replace(',', '.').split(':')
                    if len(time_parts) == 3:
                        hours = float(time_parts[0])
                        minutes = float(time_parts[1])
                        seconds = float(time_parts[2])
                        subtitle_start = hours * 3600 + minutes * 60 + seconds
                        
                        # Only include subtitles that start after the title ends
                        if subtitle_start >= start_time:
                            story_blocks.append(f"{subtitle_index}\n{time_line}\n{text}")
                            subtitle_index += 1
        
        # Write the story-only SRT file
        with open(output_srt_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(story_blocks))
        
        print(f"Created story-only SRT: {len(story_blocks)} subtitles starting from {start_time:.3f}s")
        
    except Exception as e:
        print(f"Error creating story-only SRT: {e}")
        # Fallback: copy original file
        import shutil
        shutil.copy2(original_srt_path, output_srt_path)

def get_title_end_time(captions_path, story_data):
    """
    Analyzes the SRT file to find when the title reading ends.
    
    Args:
        captions_path (str): Path to the SRT file.
        story_data (dict): Story data containing the title.
    
    Returns:
        float: Time in seconds when title ends, default 4.5 if not found.
    """
    try:
        title_words = story_data['title'].lower().split()
        if not title_words:
            return 4.5
        
        # Look for the last word of the title in the SRT file
        last_title_word = title_words[-1].rstrip('.,!?')
        
        with open(captions_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into subtitle blocks
        blocks = content.strip().split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                time_line = lines[1]
                text_line = lines[2].lower().strip()
                
                # Check if this contains the last word of the title
                if last_title_word in text_line:
                    # Extract end time
                    if '-->' in time_line:
                        end_time_str = time_line.split('-->')[1].strip()
                        # Parse HH:MM:SS,mmm format
                        time_parts = end_time_str.replace(',', '.').split(':')
                        if len(time_parts) == 3:
                            hours = float(time_parts[0])
                            minutes = float(time_parts[1])
                            seconds = float(time_parts[2])
                            total_seconds = hours * 3600 + minutes * 60 + seconds
                            # Add small buffer to ensure title is fully read
                            return total_seconds + 0.5
        
        # Fallback if parsing fails
        return 4.5
    except Exception as e:
        print(f"Warning: Could not parse title end time: {e}")
        return 4.5

def compose_final_video(background_video_path, opening_image_path, title_voice_path, story_voice_path, captions_path, output_path, opening_duration=3.0, story_data=None, background_video_path_2=None):
    """
    Composes the final video using FFmpeg with combined audio.
    Note: title_voice_path and story_voice_path now point to the same combined audio file.

    Args:
        background_video_path (str): Path to the first background Minecraft video (top half).
        opening_image_path (str): Path to the opening Reddit post image.
        title_voice_path (str): Path to the combined voiceover audio (same as story_voice_path).
        story_voice_path (str): Path to the combined voiceover audio (same as title_voice_path).
        captions_path (str): Path to the SRT caption file.
        output_path (str): Path for the output video.
        opening_duration (float): Duration to show opening image (default: 3.0 seconds).
        story_data: Story data for timing calculations.
        background_video_path_2 (str): Optional path to the second background video (bottom half).

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Find FFmpeg executable
        ffmpeg_path, ffprobe_path = find_ffmpeg_path()
        if not ffmpeg_path:
            print("FFmpeg not found. Please install FFmpeg.")
            return False
        
        # Get audio duration (both paths point to same file now)
        total_audio_duration = get_audio_duration(title_voice_path)
        
        if not total_audio_duration:
            print("Failed to get audio duration")
            return False
        
        # Get EXACT title end time by counting words in SRT file
        title_end_time = 4.5  # Default fallback
        if story_data:
            try:
                # Import the exact timing algorithm
                import sys
                sys.path.append(os.path.dirname(__file__))
                from timing_algorithms import get_title_end_time_exact
                
                title_end_time = get_title_end_time_exact(captions_path, story_data)
            except Exception as e:
                print(f"Warning: Exact timing failed, using fallback: {e}")
                # Fallback to original simple method
                title_end_time = get_title_end_time(captions_path, story_data)
        
        print(f"🎯 Title reading ends EXACTLY at: {title_end_time:.3f} seconds")
        
        # Use fixed opening duration, then remaining time for background
        actual_opening_duration = max(opening_duration, 3.0)  # Minimum 3 seconds
        background_duration = total_audio_duration - actual_opening_duration
        
        print(f"Total audio duration: {total_audio_duration:.2f} seconds")
        print(f"Opening image duration: {actual_opening_duration:.2f} seconds")
        print(f"Background video duration: {background_duration:.2f} seconds")
        
        # Convert paths to use forward slashes for FFmpeg
        background_video_path = background_video_path.replace('\\', '/')
        opening_image_path = opening_image_path.replace('\\', '/')
        combined_voice_path = title_voice_path.replace('\\', '/')  # Use combined audio
        output_path = output_path.replace('\\', '/')
        
        # Handle second background video path if provided
        if background_video_path_2:
            background_video_path_2 = background_video_path_2.replace('\\', '/')
        
        # Create temp video without subtitles first
        temp_video = output_path.replace('.mp4', '_temp.mp4')
        
        # Prepare FFmpeg command based on whether we have one or two background videos
        if background_video_path_2:
            # Step 1: Create video with two stacked background videos
            cmd1 = [
                ffmpeg_path, "-y",  # Overwrite output file
                
                # Input 0: First background video (top half)
                "-i", background_video_path,
                
                # Input 1: Second background video (bottom half)
                "-i", background_video_path_2,
                
                # Input 2: Reddit post image
                "-loop", "1", "-i", opening_image_path,
                
                # Input 3: Combined audio (full audio track)
                "-i", combined_voice_path,
                
                # Filter complex: stack two background videos and overlay post image
                "-filter_complex",
                f"[0:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[bg1];"
                f"[1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[bg2];"
                f"[bg1][bg2]vstack=inputs=2[bg_stacked];"
                f"[2:v]scale=1000:-1:force_original_aspect_ratio=decrease[post];"
                f"[bg_stacked][post]overlay=(W-w)/2:(H-h)/2:enable='between(t,0,{title_end_time})'[video]",
                
                # Map the video and audio
                "-map", "[video]", "-map", "3:a",
                
                # FAST encoding settings - prioritize speed over quality
                "-c:v", "libx264", 
                "-preset", "ultrafast",   # Fastest encoding preset
                "-crf", "23",             # Reasonable quality, much faster
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                
                # Audio settings
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                
                # Duration (match total audio duration)
                "-t", str(total_audio_duration),
                
                # Output temp video
                temp_video
            ]
        else:
            # Step 1: Create video with single background video (original behavior)
            cmd1 = [
                ffmpeg_path, "-y",  # Overwrite output file
                
                # Input 0: Background video (main video throughout)
                "-i", background_video_path,
                
                # Input 1: Reddit post image
                "-loop", "1", "-i", opening_image_path,
                
                # Input 2: Combined audio (full audio track)
                "-i", combined_voice_path,
                
                # Filter complex: background video with fast scaling
                "-filter_complex",
                f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[bg];"
                f"[1:v]scale=1000:-1:force_original_aspect_ratio=decrease[post];"
                f"[bg][post]overlay=(W-w)/2:(H-h)/2:enable='between(t,0,{title_end_time})'[video]",
                
                # Map the video and audio
                "-map", "[video]", "-map", "2:a",
                
                # FAST encoding settings - prioritize speed over quality
                "-c:v", "libx264", 
                "-preset", "ultrafast",   # Fastest encoding preset
                "-crf", "23",             # Reasonable quality, much faster
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                
                # Audio settings
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                
                # Duration (match total audio duration)
                "-t", str(total_audio_duration),
                
                # Output temp video
                temp_video
            ]
        
        print("Running FFmpeg command (Step 1: Video without subtitles)...")
        print(f"Command: {' '.join(cmd1)}")
        try:
            result = subprocess.run(cmd1, capture_output=True, text=True, check=True, timeout=300)  # 5 minute timeout
            print("Step 1 completed successfully!")
        except subprocess.TimeoutExpired:
            print("FFmpeg timed out after 5 minutes - killing process...")
            return False
        
        # Step 2: Add subtitles to the video (only after title ends)
        # Note: FFmpeg subtitles filter doesn't support enable option, so we use drawtext
        rel_captions_path = os.path.relpath(captions_path).replace('\\', '/')
        
        # Create a modified SRT file that starts from title_end_time
        temp_srt_path = captions_path.replace('.srt', '_story_only.srt')
        create_story_only_srt(captions_path, temp_srt_path, title_end_time)
        rel_temp_srt = os.path.relpath(temp_srt_path).replace('\\', '/')
        
        cmd2 = [
            ffmpeg_path, "-y",
            "-i", temp_video,
            "-vf", f"subtitles='{rel_temp_srt}':force_style='Fontname=Arial,Fontsize=26,Bold=1,PrimaryColour=&H0000ffff,OutlineColour=&H00000000,Outline=2,Shadow=2,Alignment=2,MarginV=120'",
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-c:a", "copy",  # Copy audio without re-encoding
            output_path
        ]
        
        print("Running FFmpeg command (Step 2: Adding subtitles)...")
        try:
            result = subprocess.run(cmd2, capture_output=True, text=True, check=True, timeout=300)  # 5 minute timeout
        except subprocess.TimeoutExpired:
            print("FFmpeg subtitle step timed out after 5 minutes - killing process...")
            return False
        
        # Clean up temp file
        if os.path.exists(temp_video):
            os.remove(temp_video)
            
        print("Video composition completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        print(f"FFmpeg stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error during video composition: {e}")
        return False

def main(background_video_filename=None, background_video_filename_2=None):
    """
    Main function to compose the final video from the latest generated assets.

    Args:
        background_video_filename (str): Optional specific background video filename for top half.
        background_video_filename_2 (str): Optional specific background video filename for bottom half.
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
    
    # Get background video(s)
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
        print(f"Using background video (top): {video_files[0]}")
    
    # Get second background video if specified
    background_video_path_2 = None
    if background_video_filename_2:
        background_video_path_2 = os.path.join(background_dir, background_video_filename_2)
        if not os.path.exists(background_video_path_2):
            print(f"Specified second background video not found: {background_video_filename_2}")
            return
        print(f"Using second background video (bottom): {background_video_filename_2}")
    elif background_video_filename:
        print("Note: Using single background video. Specify --background2 for split-screen effect.")
    
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
    if background_video_path_2:
        print(f"Background 2: {os.path.basename(background_video_path_2)}")
    print(f"Output: {output_filename}")
    
    # Compose the video
    success = compose_final_video(
        background_video_path=background_video_path,
        opening_image_path=image_file,
        title_voice_path=title_voice_file,
        story_voice_path=story_voice_file,
        captions_path=caption_file,
        output_path=output_path,
        background_video_path_2=background_video_path_2
    )
    
    if success:
        print(f"🎉 Success! Final video saved to: {output_path}")
        print(f"Video includes title voiceover during opening image!")
        print(f"Video is ready for upload to TikTok, Instagram Reels, YouTube Shorts!")
    else:
        print("❌ Failed to compose final video.")

if __name__ == "__main__":
    import sys
    
    # Allow passing background video filenames as arguments
    background_video = sys.argv[1] if len(sys.argv) > 1 else None
    background_video_2 = sys.argv[2] if len(sys.argv) > 2 else None
    main(background_video, background_video_2)
