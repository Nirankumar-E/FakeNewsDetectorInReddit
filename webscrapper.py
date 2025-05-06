from duckduckgo_search import DDGS
from newspaper import Article

query = input("Enter a topic or URL: ")

# Step 1: Perform search using DuckDuckGo
with DDGS() as ddgs:
    results = ddgs.text(query, max_results=5)

# Step 2: Extract article content
for i, result in enumerate(results, 1):
    url = result.get('href') or result.get('url')
    if not url:
        continue

    print(f"\n🔗 Result {i}: {url}")

    try:
        article = Article(url)
        article.download()
        article.parse()
        print(f"\n📰 Title: {article.title}")
        print(f"\n📄 Content:\n{article.text[:1000]}...\n")
    except Exception as e:
        print(f"Failed to parse: {e}")
