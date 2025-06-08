import os
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path

# Print current working directory and check for .env file
current_dir = Path.cwd()
print(f"Current working directory: {current_dir}")
env_path = current_dir / '.env'
print(f".env file exists: {env_path.exists()}")

if env_path.exists():
    print("\nContents of .env file:")
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print("Raw content:")
        print(repr(content))  # This will show any hidden characters
        print("\nProcessed content:")
        print(content)
        
        # Try to set environment variables manually
        for line in content.splitlines():
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                print(f"Setting {key} = {value}")
                os.environ[key] = value

# Try loading with different methods
print("\nTrying different loading methods:")
# Method 1: Direct load
load_dotenv(env_path, override=True)

# Method 2: Load with explicit encoding
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip()

# Debug: Print all environment variables
print("\nEnvironment variables after loading:")
print(f"NEWS_API_KEY exists: {'NEWS_API_KEY' in os.environ}")
print(f"OPENAI_API_KEY exists: {'OPENAI_API_KEY' in os.environ}")

if 'NEWS_API_KEY' in os.environ:
    print(f"NEWS_API_KEY value: {os.environ['NEWS_API_KEY']}")
if 'OPENAI_API_KEY' in os.environ:
    print(f"OPENAI_API_KEY value: {os.environ['OPENAI_API_KEY']}")

class NewsScraper:
    def __init__(self):
        # Direct API key for testing
        self.api_key = "6c52cd8896cd4865b3f02ea494bcec78"  # NewsAPI key
        print(f"\nNews API Key found: {bool(self.api_key)}")
        if not self.api_key:
            raise ValueError("NEWS_API_KEY not found")
        self.newsapi = NewsApiClient(api_key=self.api_key)

    def get_trending_news(self, category='general', language='en', max_articles=5):
        """
        Fetch trending news articles from NewsAPI
        """
        try:
            # Get news from the last 24 hours
            from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Get top headlines
            headlines = self.newsapi.get_top_headlines(
                category=category,
                language=language,
                page_size=max_articles
            )

            if headlines['status'] != 'ok':
                raise Exception(f"NewsAPI Error: {headlines.get('message', 'Unknown error')}")

            articles = headlines['articles']
            
            # Process and clean articles
            processed_articles = []
            for article in articles:
                if article['title'] and article['description']:
                    # Clean and format the article data
                    processed_article = {
                        'title': article['title'].strip(),
                        'description': article['description'].strip(),
                        'url': article['url'],
                        'image_url': article['urlToImage'] if article['urlToImage'] else None,
                        'source': article['source']['name'],
                        'published_at': article['publishedAt']
                    }
                    
                    # Print article details for debugging
                    print(f"\nProcessing article: {processed_article['title']}")
                    print(f"Description: {processed_article['description']}")
                    print(f"Image URL: {processed_article['image_url']}")
                    
                    processed_articles.append(processed_article)

            return processed_articles

        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return []

    def get_article_content(self, article):
        """
        Get the full content of an article
        """
        return {
            'title': article['title'],
            'description': article['description'],
            'source': article['source'],
            'url': article['url'],
            'image_url': article['image_url']
        } 