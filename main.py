import re
import nltk
import praw
import pandas as pd
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

# -------------------- NLTK SETUP --------------------
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# -------------------- TEXT CLEANING --------------------
def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = text.lower()
    return " ".join([word for word in text.split() if word not in stop_words])

# -------------------- REDDIT SETUP --------------------
reddit = praw.Reddit(
    client_id='Ipx5c-T6JmfNOqZXJ8KBkQ',
    client_secret='Hdmx5kPxc6B6HkqQZZQtb99CWf_qqw',
    user_agent='fake-news-detector/1.0'
)

def search_reddit_headline(headline, subreddit='all', limit=10):
    matches = []
    try:
        for submission in reddit.subreddit(subreddit).search(headline, limit=limit):
            matches.append(submission.title)
            print(f" Title: {submission.title}")
            print(f" Score: {submission.score}")
            print(f" Comments: {submission.num_comments}")
            print(f" URL: {submission.url}\n")
    except Exception as e:
        print(f"Error fetching Reddit data: {e}")
    return matches

# -------------------- MODEL CLASS --------------------
class FakeNewsModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
        self.model = LogisticRegression(max_iter=1000)

    def train(self, df):
        # Remove class '2' (assumed noise) and use only '0' and '1'
        df = df[df['label'].isin([0, 1])]  # Filter only real/fake
        df['cleaned'] = df['text'].apply(clean_text)
        X = df['cleaned']
        y = df['label']

        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_val_vec = self.vectorizer.transform(X_val)

        self.model.fit(X_train_vec, y_train)
        y_pred = self.model.predict(X_val_vec)
        y_proba = self.model.predict_proba(X_val_vec)[:, 1]

        print("\n Model Evaluation:")
        print(classification_report(y_val, y_pred))
        print("ROC-AUC Score:", roc_auc_score(y_val, y_proba))

    def predict(self, text_list):
        vec = self.vectorizer.transform(text_list)
        return self.model.predict(vec), self.model.predict_proba(vec)[:, 1]

# -------------------- MAIN PROGRAM --------------------
def main():
    try:
        df = pd.read_csv('datas/XY_train.csv')
        print(" Dataset loaded successfully.")
    except Exception as e:
        print(f" Failed to load dataset: {e}")
        return

    print(" Columns:", df.columns.tolist())
    fn_model = FakeNewsModel()
    fn_model.train(df)

    while True:
        user_input = input("\n Enter a news headline (or type 'exit'):\n> ").strip()
        if user_input.lower() == 'exit':
            print(" Exiting...")
            break

        cleaned = clean_text(user_input)
        pred_label, pred_proba = fn_model.predict([cleaned])
        label = 'REAL' if pred_label[0] == 0 else 'FAKE'

        print(f"\n ML Prediction: {label} (Confidence: {pred_proba[0]:.2f})")
        print("\n Searching Reddit for related posts...")
        matches = search_reddit_headline(user_input)

        if matches:
            print(" Reddit has related content — likely real.")
        else:
            print(" No similar Reddit posts — possibly fake or new.")

# -------------------- RUN SCRIPT --------------------
if __name__ == '__main__':
    main()


