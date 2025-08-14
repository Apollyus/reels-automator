
# Render Opening Reddit Post Image

This script is responsible for rendering an image of a Reddit post from a story.

## Dependencies

This script requires the `imgkit` Python library and `wkhtmltoimage`.

- **imgkit**: You can install this library using pip:
  ```bash
  pip install imgkit
  ```
- **wkhtmltoimage**: This is a command-line tool that `imgkit` uses to render HTML to an image. You need to download it from [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html). The path to the executable is hardcoded in the script, so you need to make sure it is installed in `C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe`.

## Functions

### `get_latest_story_file()`

This function finds the most recently created story file in the `stories/` directory.

#### Returns

- `str`: The path to the latest story file.
- `None`: If the `stories/` directory does not exist or is empty.

### `render_post_image(story_data)`

This function takes a story and renders it as a PNG image. It uses an HTML template (`templates/reddit_post.html`) and a CSS file (`templates/reddit_post.css`) to style the image.

#### Parameters

- `story_data` (dict): The story to be rendered.

## Usage

To run this script, execute the following command in your terminal:

```bash
.venv\Scripts\activate
python src/render_post_image.py
```

This will take the latest story from the `stories/` directory and render it as a PNG image in the `images/` directory. The filename will be a timestamp followed by `_title.png`, e.g., `1678886400_title.png`.
