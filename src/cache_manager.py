import os
import json
import hashlib
import shutil

def get_content_hash(content):
    """Generate a hash for content to use as cache key."""
    if isinstance(content, dict):
        content = json.dumps(content, sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()[:12]

def get_cache_paths(base_dir, content_hash, file_type):
    """Get cache file paths based on content hash."""
    cache_dir = os.path.join(base_dir, ".cache")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    if file_type == "audio":
        return os.path.join(cache_dir, f"audio_{content_hash}.mp3")
    elif file_type == "image":
        return os.path.join(cache_dir, f"image_{content_hash}.png")
    elif file_type == "captions":
        return os.path.join(cache_dir, f"captions_{content_hash}.srt")
    elif file_type == "story":
        return os.path.join(cache_dir, f"story_{content_hash}.json")
    
    return None

def cache_exists(cache_path):
    """Check if cached file exists and is valid."""
    return os.path.exists(cache_path) and os.path.getsize(cache_path) > 0

def copy_from_cache(cache_path, target_path):
    """Copy file from cache to target location."""
    try:
        shutil.copy2(cache_path, target_path)
        return True
    except Exception as e:
        print(f"Error copying from cache: {e}")
        return False

def save_to_cache(source_path, cache_path):
    """Save file to cache."""
    try:
        shutil.copy2(source_path, cache_path)
        return True
    except Exception as e:
        print(f"Error saving to cache: {e}")
        return False

def get_story_cache_key(story_data):
    """Generate cache key for story data."""
    # Use title + story content for cache key
    content = f"{story_data['title']}{story_data['story']}"
    return get_content_hash(content)
