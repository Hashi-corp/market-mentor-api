import requests
from bs4 import BeautifulSoup
import feedparser
from app.models.news_models import NewsArticle
from datetime import datetime
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def summarize_with_groq(text: str, max_length: int = 150) -> str:
    """Use Groq API to summarize news article text"""
    if not GROQ_API_KEY or not text.strip():
        return text[:max_length] + "..." if len(text) > max_length else text
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a financial news summarizer. Provide ONLY the summary content in 4-5 clear, concise sentences. Focus on key financial information, stock impact, and important developments. Do not include phrases like 'Here is a summary' or 'The article discusses'. Start directly with the summary content."
                },
                {
                    "role": "user", 
                    "content": f"Summarize this financial news article:\n\n{text[:1000]}"  # Limit input text
                }
            ],
            "max_tokens": 100,
            "temperature": 0.3
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                summary = data['choices'][0]['message']['content'].strip()
                return summary if summary else text[:max_length] + "..."

    except Exception as e:
        print(f"Groq summarization error: {e}")
    
    # Fallback to truncation
    return text[:max_length] + "..." if len(text) > max_length else text


def get_stock_news(symbol: str, limit: int = 10) -> List[NewsArticle]:
    """
    Fetch news for a given stock symbol using RSS feeds.
    Returns a list of NewsArticle objects with title, url, published_at, source, and summary.
    """
    articles = []
    
    # Extract company name from symbol (remove .NS, .BO suffixes)
    company_query = symbol.replace('.NS', '').replace('.BO', '')
    
    # 1. Economic Times RSS
    try:
        et_rss_url = "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms"
        feed = feedparser.parse(et_rss_url)
        for entry in feed.entries[:limit//4]:
            if company_query.lower() in entry.title.lower() or company_query.lower() in entry.get('summary', '').lower():
                original_summary = entry.get('summary', '')
                summarized = summarize_with_groq(original_summary)
                articles.append(NewsArticle(
                    title=entry.title,
                    url=entry.link,
                    published_at=datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') and entry.published_parsed else datetime.utcnow(),
                    source="Economic Times",
                    summary=summarized
                ))
    except Exception as e:
        print(f"Economic Times RSS error: {e}")

    # 2. Moneycontrol RSS
    try:
        mc_rss_url = "http://www.moneycontrol.com/rss/results.xml"
        feed = feedparser.parse(mc_rss_url)
        for entry in feed.entries[:limit//4]:
            if company_query.lower() in entry.title.lower() or company_query.lower() in entry.get('summary', '').lower():
                original_summary = entry.get('summary', '')
                summarized = summarize_with_groq(original_summary)
                articles.append(NewsArticle(
                    title=entry.title,
                    url=entry.link,
                    published_at=datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') and entry.published_parsed else datetime.utcnow(),
                    source="Moneycontrol",
                    summary=summarized
                ))
    except Exception as e:
        print(f"Moneycontrol RSS error: {e}")

    # 3. Business Standard RSS
    try:
        bs_rss_url = "https://www.business-standard.com/rss/markets-106.rss"
        feed = feedparser.parse(bs_rss_url)
        for entry in feed.entries[:limit//4]:
            if company_query.lower() in entry.title.lower() or company_query.lower() in entry.get('summary', '').lower():
                original_summary = entry.get('summary', '')
                summarized = summarize_with_groq(original_summary)
                articles.append(NewsArticle(
                    title=entry.title,
                    url=entry.link,
                    published_at=datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') and entry.published_parsed else datetime.utcnow(),
                    source="Business Standard",
                    summary=summarized
                ))
    except Exception as e:
        print(f"Business Standard RSS error: {e}")

    # 4. Google News RSS (stock-specific)
    try:
        google_news_url = f"https://news.google.com/rss/search?q={company_query}+stock+share+price&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(google_news_url)
        for entry in feed.entries[:limit//4]:
            original_summary = entry.get('summary', '')
            summarized = summarize_with_groq(original_summary)
            articles.append(NewsArticle(
                title=entry.title,
                url=entry.link,
                published_at=datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') and entry.published_parsed else datetime.utcnow(),
                source="Google News",
                summary=summarized
            ))
    except Exception as e:
        print(f"Google News RSS error: {e}")

    # 5. NewsAPI functionality (if API key available)
    '''if NEWSAPI_KEY:
        try:
            params = {
                'apiKey': NEWSAPI_KEY,
                'q': f'{company_query} AND (stock OR share OR market)',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': limit//4
            }
            response = requests.get(NEWSAPI_URL, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for article in data.get('articles', []):
                    original_description = article.get('description', '')
                    summarized = summarize_with_groq(original_description)
                    articles.append(NewsArticle(
                        title=article.get('title', ''),
                        url=article.get('url', ''),
                        published_at=datetime.fromisoformat(article.get('publishedAt', '').replace('Z', '+00:00')) if article.get('publishedAt') else datetime.utcnow(),
                        source=article.get('source', {}).get('name', 'NewsAPI'),
                        summary=summarized
                    ))
        except Exception as e:
            print(f"NewsAPI error: {e}")'''

    # Remove duplicates by URL and sort by date
    seen = set()
    unique_articles = []
    for article in articles:
        if article.url not in seen and article.url:
            unique_articles.append(article)
            seen.add(article.url)
    
    # Sort by published date (newest first)
    unique_articles.sort(key=lambda x: x.published_at, reverse=True)
    
    return unique_articles[:limit]
