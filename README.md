

# Fake News Detector with Reddit Verification

This Python-based project combines machine learning and Reddit search to help detect fake news headlines. It classifies a given news headline as **REAL** or **FAKE** using a trained logistic regression model, and also checks Reddit for related discussions to support the result.

## Features

* **Text Classification** using TF-IDF + Logistic Regression
* **Reddit Verification** using PRAW (Reddit API)
* **Command-Line Interface** for interactive usage
* **Cleans Text** using NLTK and regex-based preprocessing
* **Model Evaluation** with classification metrics and ROC-AUC

## Demo

```bash
> python fake_news_detector.py

Enter a news headline (or type 'exit'):
> New study reveals unexpected effects of vitamin D
```

## How It Works

1. Cleans the input text (removes links, punctuation, stopwords).
2. Classifies the cleaned headline using a trained logistic regression model.
3. Queries Reddit to find similar headlines (cross-referencing).
4. Returns:

   * **ML Prediction:** REAL or FAKE with confidence score
   * **Reddit Posts:** If related headlines are found, increases credibility

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fake-news-detector.git
cd fake-news-detector
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:

* pandas
* scikit-learn
* nltk
* praw
* torch (if used with future ML models)

### 3. Prepare Dataset

Ensure your dataset is named `XY_train.csv` and placed inside a folder called `datas/`.

* Format:

  * `text`: the news headline/content
  * `label`: 0 for REAL, 1 for FAKE, 2 for noise (optional, filtered out in training)

### 4. Configure Reddit API

Create a Reddit App at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) and update the credentials in the script:

```python
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_SECRET',
    user_agent='fake-news-detector/1.0'
)
```

### 5. Run the Program

```bash
python fake_news_detector.py
```

## File Structure

```
fake-news-detector/
│
├── datas/
│   └── XY_train.csv            # Dataset
├── fake_news_detector.py       # Main program
├── README.md                   # Project documentation
└── requirements.txt            # Dependencies
```

## Model Details

* **Text Representation:** TF-IDF (1–2 grams, top 5000 features)
* **Classifier:** Logistic Regression
* **Evaluation:** Classification report + ROC-AUC

## License

This project is licensed under the MIT License.

## Acknowledgements

* [NLTK](https://www.nltk.org/)
* [Scikit-learn](https://scikit-learn.org/)
* [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/)
* [Reddit](https://www.reddit.com/)

---

Let me know if you'd like help creating a `requirements.txt` or Dockerizing the project.
