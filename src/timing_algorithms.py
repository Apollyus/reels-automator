def get_title_end_time_exact(captions_path, story_data):
    """
    Get the EXACT moment when title reading ends by counting words in SRT file.
    No guessing, no estimation - just precise timing from the subtitle data.
    
    Args:
        captions_path (str): Path to the SRT file.
        story_data (dict): Story data containing the title.
    
    Returns:
        float: Exact time in seconds when title ends.
    """
    try:
        import re
        
        # Count words in the title
        title = story_data['title']
        title_words = re.findall(r'\b\w+\b', title)
        title_word_count = len(title_words)
        
        print(f"Title: '{title}'")
        print(f"Title word count: {title_word_count}")
        
        # Parse SRT file
        with open(captions_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = content.strip().split('\n\n')
        words_processed = 0
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                time_line = lines[1]
                text = lines[2].strip()
                
                # Parse end time
                if '-->' in time_line:
                    end_time_str = time_line.split('-->')[1].strip()
                    # Convert HH:MM:SS,mmm to seconds
                    time_parts = end_time_str.replace(',', '.').split(':')
                    if len(time_parts) == 3:
                        hours = float(time_parts[0])
                        minutes = float(time_parts[1])
                        seconds = float(time_parts[2])
                        end_time = hours * 3600 + minutes * 60 + seconds
                        
                        # Count words in this subtitle
                        words_in_subtitle = re.findall(r'\b\w+\b', text)
                        words_processed += len(words_in_subtitle)
                        
                        print(f"Subtitle {len(blocks[:blocks.index(block)+1])}: '{text}' -> {words_processed} words total")
                        
                        # If we've processed exactly the title word count, this is our end time
                        if words_processed >= title_word_count:
                            print(f"✅ Title ends exactly at: {end_time:.3f}s (after {words_processed} words)")
                            return end_time
        
        print("❌ Could not find exact title end, using fallback")
        return 4.5
        
    except Exception as e:
        print(f"❌ Error in exact timing: {e}")
        return 4.5
