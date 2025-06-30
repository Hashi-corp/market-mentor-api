import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List

def scrape_webpage(url: str) -> str:
    """
    Scrape the content of a webpage
    
    Args:
        url: The URL to scrape
        
    Returns:
        The text content of the webpage
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Remove blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def extract_news_articles(url: str) -> List[Dict[str, Any]]:
    """
    Extract news articles from a financial news website
    
    Args:
        url: The URL of the financial news website
        
    Returns:
        A list of dictionaries containing article information
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a placeholder implementation
        # You would need to customize this for each news website
        articles = []
        
        # Example: finding article elements (would need customization)
        article_elements = soup.find_all("article") or soup.find_all("div", class_="article")
        
        for article in article_elements[:5]:  # Limiting to 5 articles
            title_element = article.find("h2") or article.find("h3")
            link_element = article.find("a")
            
            if title_element and link_element:
                title = title_element.text.strip()
                link = link_element.get("href", "")
                
                # Make relative URLs absolute
                if link and not link.startswith(("http://", "https://")):
                    link = f"{url.rstrip('/')}/{link.lstrip('/')}"
                
                articles.append({
                    "title": title,
                    "url": link,
                    "source": url
                })
        
        return articles
    
    except Exception as e:
        print(f"Error extracting articles from {url}: {e}")
        return []
