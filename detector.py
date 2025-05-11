import re
import joblib
from webscrapper import scrape_latest_news

# Load the pre-trained model and vectorizer
model = joblib.load("fake_news_model.pkl")  # Replace with the correct path to your model
vectorizer = joblib.load("tfidf_vectorizer.pkl")  # Replace with the correct path to your vectorizer

# Function to extract numbers and keywords from the title
def extract_details(title):
    # Replace hyphens with spaces to separate numbers and words
    title = re.sub(r'-', ' ', title)
    # Extract numbers
    numbers = re.findall(r'\d+', title)
    # Extract keywords
    keywords = re.findall(r'\b\w+\b', title.lower())
    return numbers, keywords

# Enhanced function to compare title details with scraped news
def compare_with_scraped_news(title, scraped_news):
    title_numbers, title_keywords = extract_details(title)
    for news in scraped_news:
        news_content = news['content']  # Compare only with the main content
        
        # Extract numbers from the news content
        content_numbers = re.findall(r'\d+', news_content)
        
        # Check if at least one number from the title matches exactly in the news content
        numbers_match = any(number == content_number for number in title_numbers for content_number in content_numbers)
        
        # Check if a certain percentage of keywords from the title exist in the news content
        matched_keywords = [keyword for keyword in title_keywords if keyword in news_content]
        keyword_match_ratio = len(matched_keywords) / len(title_keywords) if title_keywords else 0
        keywords_match = keyword_match_ratio >= 0.5  # At least 50% of keywords should match
        
        # Debugging: Print comparison results
        print(f"Checking news content...")
        print(f"Title numbers: {title_numbers}, Content numbers: {content_numbers}")
        print(f"Numbers match: {numbers_match}, Keywords match ratio: {keyword_match_ratio:.2f}")
        
        # Return True if either numbers or keywords match
        if numbers_match and keywords_match:
            return True
    return False  # No match found

# Main testing loop
if __name__ == "__main__":
    while True:
        test_input = input("\nEnter a Reddit news title to test (or type 'exit' to quit): ")
        if test_input.lower() == 'exit':
            print("Exiting...")
            break

        # Scrape the latest news for comparison
        # print("\nScraping the latest news for comparison...")
        scraped_news = scrape_latest_news(test_input)

        if not scraped_news:
            print("No relevant news articles found.")
            continue

        # Compare the Reddit title with scraped news
        is_matched = compare_with_scraped_news(test_input, scraped_news)

        # Predict whether the Reddit title is fake or real
        sample_tfidf = vectorizer.transform([test_input])
        sample_prediction = model.predict(sample_tfidf)

        # Adjust prediction based on comparison
        if is_matched:
            print(f"\nPrediction for Reddit title: REAL (Matched with news)")
        else:
            print(f"\nPrediction for Reddit title: {'REAL' if sample_prediction[0] == 1 else 'FAKE'} (No match found in news)")