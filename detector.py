import sys
import re
import joblib
from webscrapper import scrape_latest_news

# Load the pre-trained model and vectorizer
model = joblib.load("/home/cyberdoc/project/FakeNewsDetectorInReddit/fake_news_model.pkl")
vectorizer = joblib.load("/home/cyberdoc/project/FakeNewsDetectorInReddit/tfidf_vectorizer.pkl")

# Function to extract numbers and keywords from the title
def extract_details(title):
    title = re.sub(r'-', ' ', title)
    numbers = re.findall(r'\d+', title)
    keywords = re.findall(r'\b\w+\b', title.lower())
    return numbers, keywords

# Enhanced function to compare title details with scraped news
def compare_with_scraped_news(title, scraped_news):
    title_numbers, title_keywords = extract_details(title)
    for news in scraped_news:
        news_content = news['content']
        relevant_context = re.findall(r'(\d+)\s+(killed|dead|injured|victims|casualties)', news_content, re.IGNORECASE)
        content_numbers = [match[0] for match in relevant_context]
        numbers_match = all(number in content_numbers for number in title_numbers)
        matched_keywords = [keyword for keyword in title_keywords if keyword in news_content]
        keyword_match_ratio = len(matched_keywords) / len(title_keywords) if title_keywords else 0
        if not numbers_match:
            return False
        if keyword_match_ratio > 0.7 and numbers_match:
            return "REAL"
        elif keyword_match_ratio > 0.6 and not content_numbers:
            return "MAY BE TRUE"
    return "FAKE"

# Main logic to handle command-line input
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No input provided.")
        sys.exit(1)

    test_input = sys.argv[1]
    scraped_news = scrape_latest_news(test_input)

    if not scraped_news:
        print("No relevant news articles found.")
        sys.exit(0)

    comparison_result = compare_with_scraped_news(test_input, scraped_news)
    sample_tfidf = vectorizer.transform([test_input])
    sample_prediction = model.predict(sample_tfidf)

    if comparison_result == "MAY BE TRUE":
        print(f"\nPrediction for Reddit title: MAY BE TRUE (Keywords match strongly, but no numbers found)")
    elif comparison_result and sample_prediction[0] == 1:
        print(f"\nPrediction for Reddit title: REAL (Matched with news)")
    else:
        print(f"\nPrediction for Reddit title: FAKE")