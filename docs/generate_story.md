
# Generate Story

This script is responsible for generating a short story in the style of a Reddit post.

## Function: `generate_story()`

This is the main function in this script. It is responsible for generating the story.

### Returns

A dictionary containing the following keys:

- `title` (str): The title of the Reddit post.
- `story` (str): The body of the Reddit post.
- `subreddit` (str): The subreddit the post belongs to.
- `username` (str): The username of the author.
- `upvotes` (int): The number of upvotes the post has.

### Current Implementation

Currently, this function returns a hardcoded story. This is a placeholder for a future implementation that will call an LLM API (e.g., OpenAI, Mistral) to generate a story dynamically.

## Usage

To run this script, execute the following command in your terminal:

```bash
python src/generate_story.py
```

This will generate a new story and save it as a JSON file in the `stories/` directory. The filename will be a timestamp, e.g., `1678886400.json`.
