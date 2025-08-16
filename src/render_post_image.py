
import json
import os
import time
from playwright.sync_api import sync_playwright

def get_latest_story_file():
    """
    Gets the path to the latest story file in the 'stories' directory.

    Returns:
        str: The path to the latest story file, or None if the directory is empty.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(script_dir)
    # Build the path to the stories directory
    stories_dir = os.path.join(project_root, "stories")
    
    if not os.path.exists(stories_dir):
        return None

    files = [os.path.join(stories_dir, f) for f in os.listdir(stories_dir) if f.endswith(".json")]
    if not files:
        return None

    return max(files, key=os.path.getctime)

def render_post_image(story_data):
    """
    Renders a Reddit post image from a story.

    Args:
        story_data (dict): The story to render.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(script_dir)
    
    # Read the HTML template
    template_path = os.path.join(project_root, "templates", "reddit_post.html")
    css_path = os.path.join(project_root, "templates", "reddit_post.css")
    
    with open(template_path, "r") as f:
        html_template = f.read()
    
    with open(css_path, "r") as f:
        css_content = f.read()

    # Inject the story data into the template
    html = html_template.replace("{{subreddit}}", story_data["subreddit"])
    html = html.replace("{{username}}", story_data["username"])
    html = html.replace("{{title}}", story_data["title"])
    html = html.replace("{{story}}", story_data["story"])
    html = html.replace("{{upvotes}}", str(story_data["upvotes"]))
    
    # Replace the CSS link with inline CSS
    css_link = '<link rel="stylesheet" type="text/css" href="reddit_post.css">'
    inline_css = f'<style>{css_content}</style>'
    html = html.replace(css_link, inline_css)

    # Create the images directory if it doesn't exist
    images_dir = os.path.join(project_root, "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Render the HTML to a PNG image using Playwright
    timestamp = int(time.time())
    image_path = os.path.join(images_dir, f"{timestamp}_title.png")
    
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set viewport to match desired image size
            page.set_viewport_size({"width": 1080, "height": 600})
            
            # Set the HTML content
            page.set_content(html)
            
            # Wait for any fonts/styles to load
            page.wait_for_timeout(1000)
            
            # Take screenshot
            page.screenshot(path=image_path, full_page=True)
            
            browser.close()
            
        print(f"Image saved to {image_path}")
        return True
        
    except Exception as e:
        print(f"Error rendering image: {e}")
        print("Please make sure you have Playwright installed: pip install playwright")
        print("And install browser: playwright install chromium")
        return False

if __name__ == "__main__":
    latest_story_file = get_latest_story_file()
    if latest_story_file:
        with open(latest_story_file, "r") as f:
            story_data = json.load(f)
        render_post_image(story_data)
    else:
        print("No stories found to render.")
