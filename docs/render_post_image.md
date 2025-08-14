
# Render Opening Reddit Post Image

This script is responsible for rendering an image of a Reddit post from a story.

## Dependencies

This script requires the `pyppeteer` Python library.

- **pyppeteer**: You can install this library using pip:
  ```bash
  pip install pyppeteer
  ```

## Functions

### `get_latest_story_file()`

This function finds the most recently created story file in the `stories/` directory.

#### Returns

- `str`: The path to the latest story file.
- `None`: If the `stories/` directory does not exist or is empty.

### `render_post_image(story_data)`

This function takes a story and renders it as a PNG image. It uses an HTML template (`templates/reddit_post.html`) and a CSS file (`templates/reddit_post.css`) to style the image. This function is asynchronous.

#### Parameters

- `story_data` (dict): The story to be rendered.

## Usage

To run this script, execute the following command in your terminal:

```bash
.venv\Scripts\activate
python src/render_post_image.py
```

This will take the latest story from the `stories/` directory and render it as a PNG image in the `images/` directory. The filename will be a timestamp followed by `_title.png`, e.g., `1678886400_title.png`.
