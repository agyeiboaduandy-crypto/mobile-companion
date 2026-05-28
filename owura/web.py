"""
OWURA Web Tools - Search, fetch, and explore the internet
Free web access without API keys.
"""

import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

class WebTools:
    def __init__(self):
        pass
    
    # ============================================================
    # WEB SEARCH - Using DuckDuckGo (free, no API key)
    # ============================================================
    def search(self, query: str, num_results: int = 5) -> str:
        """Search the web using DuckDuckGo."""
        try:
            # DuckDuckGo instant answer API
            url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; OWURA/1.0)"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            lines = [f"## Search: {query}\n"]
            
            # Abstract (main answer)
            if data.get("Abstract"):
                lines.append(f"**Answer:** {data['Abstract']}")
                lines.append(f"**Source:** {data.get('AbstractSource', 'N/A')}")
                lines.append(f"**URL:** {data.get('AbstractURL', 'N/A')}")
                lines.append("")
            
            # Related topics
            if data.get("RelatedTopics"):
                lines.append("**Related:**")
                for i, topic in enumerate(data["RelatedTopics"][:num_results], 1):
                    if isinstance(topic, dict) and "Text" in topic:
                        lines.append(f"{i}. {topic['Text'][:100]}")
                        if "FirstURL" in topic:
                            lines.append(f"   {topic['FirstURL']}")
            
            # Instant answer
            if data.get("Answer"):
                lines.append(f"\n**Instant Answer:** {data['Answer']}")
            
            if len(lines) == 1:
                lines.append("No direct answer found. Try being more specific.")
            
            return "\n".join(lines)
        
        except Exception as e:
            return f"Search error: {str(e)}"
    
    # ============================================================
    # FETCH URL CONTENT
    # ============================================================
    def fetch_url(self, url: str, max_length: int = 2000) -> str:
        """Fetch and summarize URL content."""
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; OWURA/1.0)"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode("utf-8", errors="ignore")
            
            # Basic HTML stripping
            import re
            # Remove script and style tags
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
            # Remove HTML tags
            content = re.sub(r'<[^>]+>', ' ', content)
            # Clean whitespace
            content = re.sub(r'\s+', ' ', content).strip()
            
            # Truncate
            if len(content) > max_length:
                content = content[:max_length] + "..."
            
            return f"## URL Content\n\n**URL:** {url}\n\n```\n{content}\n```"
        
        except Exception as e:
            return f"Fetch error: {str(e)}"
    
    # ============================================================
    # GITHUB SEARCH
    # ============================================================
    def search_github(self, query: str, search_type: str = "repositories") -> str:
        """Search GitHub."""
        try:
            url = f"https://api.github.com/search/{search_type}?q={urllib.parse.quote(query)}&per_page=5"
            
            req = urllib.request.Request(url, headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "OWURA"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            lines = [f"## GitHub {search_type.title()}: {query}\n"]
            
            if data.get("items"):
                for item in data["items"][:5]:
                    lines.append(f"### {item['name']}")
                    lines.append(f"- {item.get('description', 'No description')[:100]}")
                    lines.append(f"- Stars: {item.get('stargazers_count', 0)} | Language: {item.get('language', 'N/A')}")
                    lines.append(f"- {item['html_url']}")
                    lines.append("")
            else:
                lines.append("No results found.")
            
            return "\n".join(lines)
        
        except Exception as e:
            return f"GitHub search error: {str(e)}"
    
    # ============================================================
    # PACKAGE SEARCH
    # ============================================================
    def search_pypi(self, query: str) -> str:
        """Search Python packages."""
        try:
            url = f"https://pypi.org/pypi/{urllib.parse.quote(query)}/json"
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "OWURA/1.0"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            info = data.get("info", {})
            
            lines = [
                f"## PyPI: {info.get('name', query)}",
                "",
                f"**Version:** {info.get('version', 'N/A')}",
                f"**Summary:** {info.get('summary', 'N/A')}",
                f"**Author:** {info.get('author', 'N/A')}",
                f"**License:** {info.get('license', 'N/A')}",
                f"**Home:** {info.get('home_page', 'N/A')}",
                "",
                f"**Install:**",
                f"```bash",
                f"pip install {info.get('name', query)}",
                f"```",
            ]
            
            return "\n".join(lines)
        
        except:
            return f"Package '{query}' not found on PyPI."
    
    def search_npm(self, query: str) -> str:
        """Search npm packages."""
        try:
            url = f"https://registry.npmjs.org/{urllib.parse.quote(query)}"
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "OWURA/1.0"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            lines = [
                f"## npm: {data.get('name', query)}",
                "",
                f"**Latest:** {data.get('dist-tags', {}).get('latest', 'N/A')}",
                f"**Description:** {data.get('description', 'N/A')}",
                f"**Author:** {data.get('author', {}).get('name', 'N/A') if isinstance(data.get('author'), dict) else data.get('author', 'N/A')}",
                "",
                f"**Install:**",
                f"```bash",
                f"npm install {data.get('name', query)}",
                f"```",
            ]
            
            return "\n".join(lines)
        
        except:
            return f"Package '{query}' not found on npm."
    
    # ============================================================
    # DOCUMENTATION SEARCH
    # ============================================================
    def search_docs(self, query: str, docs: str = "python") -> str:
        """Search documentation."""
        docs_urls = {
            "python": f"https://docs.python.org/3/search.html?q={urllib.parse.quote(query)}",
            "javascript": f"https://developer.mozilla.org/en-US/search?q={urllib.parse.quote(query)}",
            "node": f"https://nodejs.org/en/search?q={urllib.parse.quote(query)}",
            "react": f"https://react.dev/search?q={urllib.parse.quote(query)}",
            "flask": f"https://flask.palletsprojects.com/en/3.0.x/search/?q={urllib.parse.quote(query)}",
        }
        
        url = docs_urls.get(docs, docs_urls["python"])
        
        return f"## Documentation Search\n\n**Query:** {query}\n**Docs:** {docs}\n\n**Search URL:** {url}\n\nClick the link above to view results."
    
    # ============================================================
    # STACKOVERFLOW SEARCH
    # ============================================================
    def search_stackoverflow(self, query: str) -> str:
        """Search StackOverflow."""
        try:
            url = f"https://api.stackexchange.com/2.3/search?intitle={urllib.parse.quote(query)}&site=stackoverflow&sort=relevance&pagesize=5"
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "OWURA/1.0"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            lines = [f"## StackOverflow: {query}\n"]
            
            if data.get("items"):
                for item in data["items"][:5]:
                    lines.append(f"### {item['title']}")
                    lines.append(f"- Answers: {item.get('answer_count', 0)} | Score: {item.get('score', 0)}")
                    lines.append(f"- Tags: {', '.join(item.get('tags', []))}")
                    lines.append(f"- {item['link']}")
                    lines.append("")
            else:
                lines.append("No results found.")
            
            return "\n".join(lines)
        
        except Exception as e:
            return f"StackOverflow search error: {str(e)}"
    
    # ============================================================
    # WIKIPEDIA LOOKUP
    # ============================================================
    def search_wikipedia(self, query: str) -> str:
        """Search Wikipedia."""
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "OWURA/1.0"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            lines = [
                f"## Wikipedia: {data.get('title', query)}",
                "",
                data.get("extract", "No summary available."),
                "",
                f"**Read more:** {data.get('content_urls', {}).get('desktop', {}).get('page', 'N/A')}",
            ]
            
            return "\n".join(lines)
        
        except:
            return f"Article '{query}' not found on Wikipedia."
    
    # ============================================================
    # NEWS FETCHER
    # ============================================================
    def get_news(self, topic: str = "technology") -> str:
        """Get latest news."""
        try:
            # Using DuckDuckGo news
            url = f"https://duckduckgo.com/news.js?q={urllib.parse.quote(topic)}&format=json"
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            lines = [f"## Latest News: {topic}\n"]
            
            if data.get("results"):
                for item in data["results"][:5]:
                    lines.append(f"### {item.get('title', 'N/A')}")
                    lines.append(f"- {item.get('description', 'N/A')[:150]}")
                    lines.append(f"- Source: {item.get('source', 'N/A')}")
                    lines.append(f"- {item.get('url', 'N/A')}")
                    lines.append("")
            else:
                lines.append("No news found.")
            
            return "\n".join(lines)
        
        except Exception as e:
            return f"News fetch error: {str(e)}"
    
    # ============================================================
    # UV WEATHER
    # ============================================================
    def get_weather(self, city: str) -> str:
        """Get weather info."""
        try:
            url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "curl/7.64.1"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            current = data.get("current_condition", [{}])[0]
            
            lines = [
                f"## Weather: {city}",
                "",
                f"**Temperature:** {current.get('temp_C', 'N/A')}Â°C / {current.get('temp_F', 'N/A')}Â°F",
                f"**Feels Like:** {current.get('FeelsLikeC', 'N/A')}Â°C",
                f"**Condition:** {current.get('weatherDesc', [{}])[0].get('value', 'N/A')}",
                f"**Humidity:** {current.get('humidity', 'N/A')}%",
                f"**Wind:** {current.get('windspeedKmph', 'N/A')} km/h {current.get('winddir16Point', 'N/A')}",
            ]
            
            return "\n".join(lines)
        
        except Exception as e:
            return f"Weather error: {str(e)}"
    
    # ============================================================
    # IP INFO
    # ============================================================
    def get_ip_info(self) -> str:
        """Get IP information."""
        try:
            url = "https://ipinfo.io/json"
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "OWURA/1.0"
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            lines = [
                "## Your IP Information",
                "",
                f"**IP:** {data.get('ip', 'N/A')}",
                f"**City:** {data.get('city', 'N/A')}",
                f"**Region:** {data.get('region', 'N/A')}",
                f"**Country:** {data.get('country', 'N/A')}",
                f"**Org:** {data.get('org', 'N/A')}",
                f"**Location:** {data.get('loc', 'N/A')}",
            ]
            
            return "\n".join(lines)
        
        except Exception as e:
            return f"IP info error: {str(e)}"

# Global instance
_web = None

def get_web() -> WebTools:
    global _web
    if _web is None:
        _web = WebTools()
    return _web
