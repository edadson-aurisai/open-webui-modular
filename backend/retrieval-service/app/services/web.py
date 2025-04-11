import logging
import requests
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import trafilatura

from app.core.config import settings
from app.models.web import WebSearchResult

logger = logging.getLogger(__name__)


async def search_web(
    query: str,
    engine: str = "duckduckgo",
    count: int = 3,
) -> List[WebSearchResult]:
    """
    Search the web using the configured search engine
    """
    try:
        # Select the search engine
        if engine == "brave":
            results = await search_brave(query, count)
        elif engine == "serper":
            results = await search_serper(query, count)
        elif engine == "serply":
            results = await search_serply(query, count)
        elif engine == "serpapi":
            results = await search_serpapi(query, count)
        elif engine == "serpstack":
            results = await search_serpstack(query, count)
        elif engine == "searchapi":
            results = await search_searchapi(query, count)
        elif engine == "tavily":
            results = await search_tavily(query, count)
        elif engine == "jina":
            results = await search_jina(query, count)
        elif engine == "bing":
            results = await search_bing(query, count)
        elif engine == "exa":
            results = await search_exa(query, count)
        elif engine == "perplexity":
            results = await search_perplexity(query, count)
        elif engine == "kagi":
            results = await search_kagi(query, count)
        elif engine == "mojeek":
            results = await search_mojeek(query, count)
        elif engine == "bocha":
            results = await search_bocha(query, count)
        elif engine == "google_pse":
            results = await search_google_pse(query, count)
        else:
            # Default to DuckDuckGo
            results = await search_duckduckgo(query, count)
        
        return results
    except Exception as e:
        logger.error(f"Error searching web: {e}")
        raise


async def fetch_web_content(url: str) -> str:
    """
    Fetch content from a web URL
    """
    try:
        # Fetch the content
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            # Extract the main content
            content = trafilatura.extract(downloaded, include_links=True, include_images=True)
            if content:
                return content
        
        # Fallback to requests + BeautifulSoup if trafilatura fails
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Remove blank lines
        text = "\n".join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        logger.error(f"Error fetching web content: {e}")
        raise


# Implement search engine specific functions
async def search_duckduckgo(query: str, count: int) -> List[WebSearchResult]:
    """
    Search using DuckDuckGo
    """
    # This is a placeholder. In a real implementation, you would use the DuckDuckGo API
    # or scrape the results.
    return [
        WebSearchResult(
            title="DuckDuckGo Search Result",
            url="https://example.com",
            snippet="This is a placeholder for DuckDuckGo search results.",
        )
    ]


async def search_brave(query: str, count: int) -> List[WebSearchResult]:
    """
    Search using Brave Search
    """
    if not settings.brave_search_api_key:
        raise ValueError("Brave Search API key not configured")
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": settings.brave_search_api_key,
    }
    params = {
        "q": query,
        "count": count,
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    
    results = []
    for result in data.get("web", {}).get("results", []):
        results.append(
            WebSearchResult(
                title=result.get("title", ""),
                url=result.get("url", ""),
                snippet=result.get("description", ""),
            )
        )
    
    return results


# Implement other search engine functions similarly
# For brevity, I'm not implementing all of them here
