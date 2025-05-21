# FakeNewsDetectorInReddit

## Overview

**FakeNewsDetectorInReddit** is a web-based tool for verifying the authenticity of news-related Reddit posts. It uses machine learning and real-time news scraping to compare Reddit titles with actual news articles, helping to identify potentially fake or misleading information.

## Features

- Web UI (`index.php`) for easy user interaction.
- Extracts numbers and keywords from Reddit post titles.
- Scrapes real-time news articles from the web for comparison.
- Compares title details (numbers and keywords) with news content.
- Skips unrelated or excessively long news articles.
- Ignores content after "also read" sections in news articles.
- Uses a trained machine learning model (TF-IDF + classifier) for additional prediction.
- Provides clear output: `REAL`, `FAKE`, or `MAY BE TRUE`.

## How It Works

1. **Input**: Enter a Reddit post title or URL via the web UI.
2. **Scraping**: The tool scrapes the latest news articles related to the title.
3. **Comparison**: It compares numbers and keywords from the title with those in the news articles, skipping content after "also read" and ignoring articles longer than 2000 words.
4. **Prediction**: Based on the comparison and the ML model, it outputs whether the news is likely `REAL`, `FAKE`, or `MAY BE TRUE`.

## Usage

- Open `index.php` in your browser (ensure your PHP server is running).
- Enter the Reddit post title or URL and submit to get the result.

## Project Structure

- `index.php` - Web UI for user input and result display.
- `detector.py` - Main script for running the detector.
- `webscrapper.py` - Contains functions for scraping news articles.
- `fake_news_model.pkl` - Pre-trained machine learning model.
- `tfidf_vectorizer.pkl` - Pre-trained TF-IDF vectorizer.
- `README.md` - Project documentation.

## Requirements

- Python 3.x
- PHP (for the web UI)
- `joblib`
- `requests`
- `beautifulsoup4`
- Any other dependencies listed in your environment or requirements file.

## How to Train Your Own Model

If you want to retrain the model:
1. Collect a dataset of real and fake news.
2. Train a TF-IDF vectorizer and a classifier (e.g., Logistic Regression).
3. Save the model and vectorizer as `.pkl` files using `joblib`.

## Notes

- The tool is designed for educational and research purposes.
- The accuracy depends on the quality of the scraped news and the trained model.
- Always verify critical information from trusted sources.

## License

MIT License (or your chosen license)