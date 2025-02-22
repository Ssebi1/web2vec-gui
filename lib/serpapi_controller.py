import os

from serpapi import GoogleSearch


class SerpApiController:
    def __init__(self):
        self.api_key = os.getenv("SERP_API_KEY")

    def search(self, query):
        params = {
            "q": query,
            "api_key": self.api_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        pages = []
        if "organic_results" in results:
            for res in results["organic_results"]:
                pages.append({
                    "title": res.get("title"),
                    "link": res.get("link")
                })

        return pages
