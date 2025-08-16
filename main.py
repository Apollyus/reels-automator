#!/usr/bin/env python3
"""
Minecraft Reddit Story Reels Generator - Main Pipeline
Automated pipeline that generates Reddit story videos with Minecraft parkour footage.

Usage: python main.py --count <number_of_videos> --background <background_video_filename>
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add src directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, "src")
sys.path.insert(0, src_dir)

# Import pipeline modules
try:
    from generate_story import generate_story
    from save_story_to_database import save_story_to_database, get_latest_story_file
    from render_post_image import render_post_image
    from generate_voiceover import generate_voiceover
    from generate_captions import generate_captions
    from compose_video import compose_final_video, get_audio_duration
except ImportError as e:
    print(f"Error importing pipeline modules: {e}")
    print("Please ensure all required modules are in the 'src/' directory.")
    sys.exit(1)

def check_idea_database(story_data, ideas_file="ideas/ideas.json"):
    """
    Check if a similar story idea already exists in the database.
    
    Args:
        story_data (dict): The story to check for duplicates.
        ideas_file (str): Path to the ideas database file.
    
    Returns:
        bool: True if similar idea exists, False otherwise.
    """
    import json
    import hashlib
    
    if not os.path.exists(ideas_file):
        return False
    
    try:
        with open(ideas_file, 'r', encoding='utf-8') as f:
            existing_ideas = json.load(f)
        
        # Create hash of current story title for comparison
        current_hash = hashlib.md5(story_data['title'].lower().encode()).hexdigest()
        
        # Check for similar titles (same hash or very similar)
        for idea in existing_ideas:
            if 'hash' in idea:
                existing_hash = hashlib.md5(idea.get('title', '').lower().encode()).hexdigest()
                if current_hash == existing_hash:
                    print(f"⚠️  Similar idea found: '{idea.get('title', '')}'")
                    return True
        
        return False
        
    except Exception as e:
        print(f"Error checking idea database: {e}")
        return False

def validate_background_video(background_filename):
    """
    Validate that the specified background video exists.
    
    Args:
        background_filename (str): Name of the background video file.
    
    Returns:
        str: Full path to the background video, or None if not found.
    """
    background_dir = "background"
    
    if not os.path.exists(background_dir):
        print(f"❌ Background directory '{background_dir}' not found.")
        print("Please create the directory and add Minecraft parkour videos.")
        return None
    
    background_path = os.path.join(background_dir, background_filename)
    
    if not os.path.exists(background_path):
        print(f"❌ Background video '{background_filename}' not found in '{background_dir}' directory.")
        
        # List available videos
        video_files = [f for f in os.listdir(background_dir) 
                      if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        
        if video_files:
            print("Available background videos:")
            for video in video_files:
                print(f"  - {video}")
        else:
            print("No video files found in background directory.")
        
        return None
    
    return background_path

def run_pipeline_step(step_name, step_function, *args, **kwargs):
    """
    Run a pipeline step with error handling and timing.
    
    Args:
        step_name (str): Name of the step for logging.
        step_function (callable): Function to execute.
        *args: Arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
    
    Returns:
        Any: Result of the step function, or None if failed.
    """
    print(f"\n🔄 Starting: {step_name}")
    start_time = time.time()
    
    try:
        result = step_function(*args, **kwargs)
        elapsed = time.time() - start_time
        
        if result is not None:
            print(f"✅ Completed: {step_name} ({elapsed:.2f}s)")
            return result
        else:
            print(f"❌ Failed: {step_name} - Function returned None")
            return None
            
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Failed: {step_name} ({elapsed:.2f}s)")
        print(f"   Error: {str(e)}")
        return None

def generate_single_video(background_video_path, video_number, total_videos):
    """
    Generate a single video through the complete pipeline.
    
    Args:
        background_video_path (str): Path to the background video.
        video_number (int): Current video number (for display).
        total_videos (int): Total number of videos being generated.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    print(f"\n{'='*60}")
    print(f"🎬 GENERATING VIDEO {video_number}/{total_videos}")
    print(f"{'='*60}")
    
    pipeline_start = time.time()
    
    # Step 1: Generate Story
    story_data = run_pipeline_step(
        "Step 1: Generate Story",
        generate_story
    )
    if not story_data:
        return False
    
    print(f"📖 Generated story: '{story_data.get('title', 'Unknown Title')}'")
    
    # Step 0: Check Idea Database (after generating story)
    is_duplicate = run_pipeline_step(
        "Step 0: Check Idea Database",
        check_idea_database,
        story_data
    )
    
    if is_duplicate:
        print("⚠️  Duplicate idea detected. Consider regenerating with different parameters.")
        # For now, continue anyway. In future, could regenerate automatically.
    
    # Step 2: Save Story to Database
    # First save the story to a file
    timestamp = int(time.time())
    stories_dir = "stories"
    if not os.path.exists(stories_dir):
        os.makedirs(stories_dir)
    
    story_file_path = os.path.join(stories_dir, f"{timestamp}.json")
    with open(story_file_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(story_data, f, indent=4)
    
    # Then save to idea database
    database_result = run_pipeline_step(
        "Step 2: Save Story to Idea Database",
        save_story_to_database,
        story_data
    )
    if database_result is None:
        print("⚠️  Warning: Failed to save to idea database, but continuing...")
    
    # Step 3: Render Opening Reddit Post Image
    image_path = run_pipeline_step(
        "Step 3: Render Opening Reddit Post Image",
        render_post_image,
        story_data
    )
    if not image_path:
        return False
    
    # Step 4: Generate Voiceover (title, story, and combined)
    voiceover_paths = run_pipeline_step(
        "Step 4: Generate Voiceover",
        generate_voiceover,
        story_data
    )
    if not voiceover_paths:
        return False
    
    print(f"🔊 Generated audio files:")
    print(f"   Title: {os.path.basename(voiceover_paths.get('title', 'Not found'))}")
    print(f"   Story: {os.path.basename(voiceover_paths.get('story', 'Not found'))}")
    print(f"   Combined: {os.path.basename(voiceover_paths.get('combined', 'Not found'))}")
    
    # Step 5: Generate Timed Captions
    captions_path = run_pipeline_step(
        "Step 5: Generate Timed Captions",
        generate_captions,
        story_data,
        voiceover_paths['combined'],  # Use combined audio for caption timing
        2  # words per chunk for engagement
    )
    if not captions_path:
        return False
    
    # Step 6: Compose Final Video
    exports_dir = "exports"
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    
    output_filename = f"final_{timestamp}.mp4"
    output_path = os.path.join(exports_dir, output_filename)
    
    video_success = run_pipeline_step(
        "Step 6: Compose Final Video",
        compose_final_video,
        background_video_path,
        image_path,
        voiceover_paths['title'],
        voiceover_paths['story'],
        captions_path,
        output_path
    )
    
    if video_success:
        pipeline_elapsed = time.time() - pipeline_start
        print(f"\n🎉 SUCCESS! Video {video_number}/{total_videos} completed!")
        print(f"📁 Output: {output_path}")
        print(f"⏱️  Total time: {pipeline_elapsed:.2f} seconds")
        
        # Get video duration for summary
        try:
            duration = get_audio_duration(voiceover_paths['combined'])
            if duration:
                print(f"🎬 Video duration: {duration:.2f} seconds")
        except:
            pass
        
        return True
    else:
        print(f"❌ Failed to generate video {video_number}/{total_videos}")
        return False

def main():
    """
    Main function to run the complete pipeline.
    """
    parser = argparse.ArgumentParser(
        description="Minecraft Reddit Story Reels Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --count 1 --background minecraft_parkour.mp4
  python main.py --count 5 --background parkour_loop.mp4
  
Make sure to:
1. Add background videos to 'background/' directory
2. Set ELEVENLABS_API_KEY in .env file
3. Install required dependencies
        """
    )
    
    parser.add_argument(
        "--count",
        type=int,
        required=True,
        help="Number of videos to generate in one run"
    )
    
    parser.add_argument(
        "--background",
        type=str,
        required=True,
        help="Filename of the background video from the 'background/' directory"
    )
    
    parser.add_argument(
        "--words-per-chunk",
        type=int,
        default=2,
        help="Number of words per caption chunk (1=single word, 2=minimal, 3-4=balanced)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.count < 1:
        print("❌ Error: --count must be at least 1")
        sys.exit(1)
    
    if args.words_per_chunk < 1 or args.words_per_chunk > 8:
        print("❌ Error: --words-per-chunk must be between 1 and 8")
        sys.exit(1)
    
    # Validate background video
    background_video_path = validate_background_video(args.background)
    if not background_video_path:
        sys.exit(1)
    
    # Print startup information
    print("🚀 Minecraft Reddit Story Reels Generator")
    print("=" * 50)
    print(f"📊 Generating {args.count} video(s)")
    print(f"🎮 Background video: {args.background}")
    print(f"📝 Words per caption: {args.words_per_chunk}")
    print(f"📁 Background path: {background_video_path}")
    
    # Check dependencies
    print(f"\n🔍 Checking dependencies...")
    
    # Check .env file
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found. Make sure ELEVENLABS_API_KEY is set.")
    
    # Check required directories
    required_dirs = ['stories', 'voices', 'images', 'captions', 'exports', 'ideas']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"📁 Created directory: {dir_name}")
    
    # Run pipeline for each video
    successful_videos = 0
    failed_videos = 0
    start_time = time.time()
    
    for video_num in range(1, args.count + 1):
        success = generate_single_video(background_video_path, video_num, args.count)
        
        if success:
            successful_videos += 1
        else:
            failed_videos += 1
        
        # Brief pause between videos
        if video_num < args.count:
            print("\n⏸️  Pausing 2 seconds before next video...")
            time.sleep(2)
    
    # Final summary
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"🏁 PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successful videos: {successful_videos}")
    print(f"❌ Failed videos: {failed_videos}")
    print(f"⏱️  Total execution time: {total_time:.2f} seconds")
    
    if successful_videos > 0:
        avg_time = total_time / successful_videos
        print(f"📊 Average time per video: {avg_time:.2f} seconds")
        print(f"📁 Videos saved to: exports/")
        print(f"🎯 Ready for upload to TikTok, Instagram Reels, YouTube Shorts!")
    
    if failed_videos > 0:
        print(f"\n⚠️  {failed_videos} video(s) failed. Check error messages above.")
        sys.exit(1)
    else:
        print(f"\n🎉 All videos generated successfully!")

if __name__ == "__main__":
    main()
