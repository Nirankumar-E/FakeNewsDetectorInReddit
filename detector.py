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
    numbers_match_results = []  # List to track numbers match results
    keyword_match_ratios = []  # List to track keyword match ratios

    for idx, news in enumerate(scraped_news):
        news_content = news['content']

        # Truncate content from the point where "also read" appears
        if "also read" in news_content.lower():
            news_content = news_content[:news_content.lower().find("also read")]
            print(f"[DEBUG] Truncated content at 'also read' for article {idx + 1}/{len(scraped_news)}")

        # Skip articles with content length greater than 2000 words
        if len(news_content.split()) > 2000:
            print(f"[DEBUG] Skipping article {idx + 1}/{len(scraped_news)} due to content length: {len(news_content.split())} words")
            continue

        # Debugging output for each article
        print(f"\n[DEBUG] Processing article {idx + 1}/{len(scraped_news)}")
        print(f"Full content length: {len(news_content.split())} words")
        print(f"Full content preview: {news_content[:500]}...")  # Print the first 500 characters for preview

        # Extract all numbers from content
        content_numbers = re.findall(r'\d+', news_content)

        # Filter out numbers that are unrelated (e.g., years or unrelated incidents)
        filtered_numbers = [num for num in content_numbers if len(num) < 4 or int(num) < 2100]
        print(f"Filtered content numbers: {filtered_numbers}")

        # Debugging output for extracted numbers
        print(f"Title numbers: {title_numbers}")
        print(f"Content numbers: {filtered_numbers}")

        # Compare numbers and keywords
        numbers_match = all(number in filtered_numbers for number in title_numbers)
        matched_keywords = [keyword for keyword in title_keywords if keyword in news_content.lower()]
        keyword_match_ratio = len(matched_keywords) / len(title_keywords) if title_keywords else 0

        # Append results to tracking lists
        numbers_match_results.append(numbers_match)
        keyword_match_ratios.append(keyword_match_ratio)

        # Debugging output for matching results
        print(f"Numbers match: {numbers_match}")
        print(f"Keyword match ratio: {keyword_match_ratio}")

    # Analyze results after processing all articles
    true_count = numbers_match_results.count(True)
    false_count = numbers_match_results.count(False)
    max_keyword_match_ratio = max(keyword_match_ratios) if keyword_match_ratios else 0

    print(f"\n[DEBUG] Numbers match results: {numbers_match_results}")
    print(f"[DEBUG] True count: {true_count}, False count: {false_count}")
    print(f"[DEBUG] Max keyword match ratio: {max_keyword_match_ratio}")

    # Decision logic based on majority and keyword match ratio
    if false_count > true_count:
        print("[DEBUG] Majority of numbers match results are False. Returning FAKE.")
        return False
    elif true_count > false_count and max_keyword_match_ratio > 0.6:
        print("[DEBUG] Majority of numbers match results are True and keyword match ratio is above 0.6. Returning REAL.")
        return "REAL"
    else:
        print("[DEBUG] No strong majority or insufficient keyword match ratio. Returning FAKE.")
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
