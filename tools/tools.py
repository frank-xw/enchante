from langchain.serpapi import SerpAPIWrapper


def get_profile_url(text: str) -> str:
    """Search for Linkedin Profile Page."""
    search = SerpAPIWrapper()
    res = search.run(f"{text}")

    return res
