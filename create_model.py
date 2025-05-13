import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re


try:
    print("Loading datasets...")
    fake = pd.read_csv("Fake.csv")  
    real = pd.read_csv("True.csv")  
    fake['label'] = 0
    real['label'] = 1
    data = pd.concat([fake, real]).sample(frac=1, random_state=42)
    print("Datasets loaded and combined successfully!")
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

print("Preprocessing data...")

# label the column names as title and label for processing otherwise it will return the error
if 'title' not in data.columns or 'label' not in data.columns:
    print("Error: Dataset must contain 'title' and 'label' columns.")
    exit()

def clean_text(text):
    text = re.sub(r'\W', ' ', text)  
    text = re.sub(r'\s+', ' ', text)  
    return text.lower()

data['title'] = data['title'].apply(clean_text)

X = data['title']
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(max_features=5000)  
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("Training the model...")
model = LogisticRegression(class_weight='balanced')
model.fit(X_train_tfidf, y_train)

print("Evaluating the model...")
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["FAKE", "REAL"]))

print("Saving the model and vectorizer...")
joblib.dump(model, "fake_news_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("Model and vectorizer saved successfully!")