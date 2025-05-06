import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re

# Load and Combine the Datasets
try:
    print("Loading datasets...")
    fake = pd.read_csv("Fake.csv")  
    real = pd.read_csv("True.csv") 

    # labeling the data set : 0 for fake, 1 for real
    fake['label'] = 0
    real['label'] = 1

    # Combining the datasets and shuffled for randomness
    data = pd.concat([fake, real]).sample(frac=1, random_state=42)  
    print("Datasets loaded and combined successfully!")
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Preprocess the Data
print("Preprocessing data...")

# Checkin whethet the dataset has the required columns "label" and "title"
if 'title' not in data.columns or 'label' not in data.columns:
    print("Error: Dataset must contain 'title' and 'label' columns.")
    exit()

# Clean the text data
def clean_text(text):
    text = re.sub(r'\W', ' ', text)  
    text = re.sub(r'\s+', ' ', text)  
    return text.lower()

data['title'] = data['title'].apply(clean_text)

# Using the "title" column as the text data and obviously "label" represents value 0 or 1
X = data['title']
y = data['label']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data into numerical features using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)  # Limit to top 5000 features
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Step 3: Train the Model
print("Training the model...")
model = LogisticRegression(class_weight='balanced')  # Handle class imbalance
model.fit(X_train_tfidf, y_train)

# Step 4: Evaluate the Model
print("Evaluating the model...")
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["FAKE", "REAL"]))

# Step 5: Save the Model and Vectorizer
print("Saving the model and vectorizer...")
joblib.dump(model, "fake_news_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("Model and vectorizer saved successfully!")

# Step 6: Test the Model with a Sample Input (Optional)
while True:
    test_input = input("\nEnter a news title to test (or type 'exit' to quit): ")
    if test_input.lower() == 'exit':
        print("Exiting...")
        break
    sample_tfidf = vectorizer.transform([test_input])
    sample_prediction = model.predict(sample_tfidf)
    print(f"Prediction: {'REAL' if sample_prediction[0] == 1 else 'FAKE'}")