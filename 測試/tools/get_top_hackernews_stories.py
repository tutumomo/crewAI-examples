import json
import httpx
from langchain.tools import tool

class GetTopHackernewsStories():
 
    @tool("Get top stories from Hacker News.")
    def get_top_hackernews_stories(tool_input={}, num_stories: int = 10) -> str:
        """Use this function to get top stories from Hacker News.
        Args:
            tool_input (dict): Input parameter required by the @tool decorator. Defaults to an empty dictionary.
            num_stories (int): Number of stories to return. Defaults to 10.
        Returns:
            str: JSON string of top stories.
        """
        try:
            # Fetch top story IDs
            response = httpx.get('https://hacker-news.firebaseio.com/v0/topstories.json')
            response.raise_for_status()
            story_ids = response.json()

            # Fetch story details
            stories = []
            for story_id in story_ids[:num_stories]:
                story_response = httpx.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
                story_response.raise_for_status()
                story = story_response.json()
                if "text" in story:
                    story.pop("text", None)
                stories.append(story)
            return json.dumps(stories)
        except Exception as e:
            print(f"An error occurred: {e}")
            return json.dumps({"error": "An error occurred while fetching Hacker News stories."})

# Example usage
# top_stories = GetTopHackernewsStories.get_top_hackernews_stories({})
# print(top_stories)
