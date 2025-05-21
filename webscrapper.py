import requests
from bs4 import BeautifulSoup
from newspaper import Article
from newspaper.configuration import Configuration
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def google_news_search(query, max_results=5):
    search_url = f"https://www.google.com/search?q={query}&tbm=nws&hl=en&gl=in&num={max_results}"
    response = requests.get(search_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"[ERROR] Google News search failed: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    result_urls = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/url?q="):
            url = href.split("/url?q=")[1].split("&")[0]
            if url.startswith("http"):
                result_urls.append(url)

    return result_urls[:max_results]

def parse_article(url):
    try:
        config = Configuration()
        config.browser_user_agent = HEADERS["User-Agent"]
        config.request_timeout = 10

        article = Article(url, config=config)
        article.download()
        article.parse()
        return {"title": article.title, "content": article.text}
    except Exception as e:
        # print(f"[ERROR] Failed to parse")
        return None

def scrape_latest_news(query, max_results=5):
    print(f"Gathering Real-Time News for: {query}")
    urls = google_news_search(query, max_results)
    articles = []
    for url in urls:
        # print(f"[DEBUG] Found URL: ")
        article = parse_article(url)
        if article:
            # print(f"[INFO] Title: {article['title']}")
            # print(f"[INFO] Content: {article['content'][:1000]}...")  # Print first 1000 chars of content for preview
            articles.append(article)
        time.sleep(1)  # To avoid hitting Google too fast
    return articles
