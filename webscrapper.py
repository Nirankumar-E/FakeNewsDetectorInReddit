from newspaper import Article
from newspaper.configuration import Configuration
from duckduckgo_search import DDGS

def scrape_latest_news(query, max_results=5):
    results_list = []
    try:
        # Step 1: Perform a DuckDuckGo search
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            for result in results:
                url = result.get('href') or result.get('url')
                if url:
                    print(f"Found URL: {url}")
                    # Step 2: Parse the article
                    article_data = parse_news_content(url)
                    if article_data:
                        results_list.append(article_data)
        if not results_list:
            print("No relevant news articles found.")
    except Exception as e:
        print(f"Failed to scrape news: {e}")
    return results_list

def parse_news_content(url):
    try:
        # Configure custom headers
        config = Configuration()
        config.browser_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        
        # Initialize the Article object with the URL and custom configuration
        article = Article(url, config=config)
        
        # Download and parse the article
        article.download()
        article.parse()
        
        # Return the title and content of the article
        return {"title": article.title, "content": article.text}
    except Exception as e:
        print(f"Failed to parse the article from {url}: {e}")
        return None