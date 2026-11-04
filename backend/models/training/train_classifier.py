import pandas as pd
import joblib

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Project paths
BASE_DIR = Path(__file__).resolve().parents[3]

DATASET_DIR = BASE_DIR / "dataset" / "processed"
MODEL_DIR = BASE_DIR / "backend" / "models" / "saved"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# Load datasets
train_df = pd.read_parquet(DATASET_DIR / "train_processed.parquet")
val_df = pd.read_parquet(DATASET_DIR / "validation_processed.parquet")


# Separate text and labels
X_train = train_df["review_text"]
y_train = train_df["label"]

X_val = val_df["review_text"]
y_val = val_df["label"]


# Convert text into numerical features
vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)


# Train Logistic Regression
model = LogisticRegression(max_iter=1000)

model.fit(X_train_tfidf, y_train)


# Evaluate on validation data
predictions = model.predict(X_val_tfidf)

accuracy = accuracy_score(y_val, predictions)

print("\nValidation Results")
print("------------------")
print("Accuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(classification_report(
    y_val,
    predictions,
    target_names=["Human-written", "AI-generated"]
))


# Save model and vectorizer
joblib.dump(model, MODEL_DIR / "review_classifier.pkl")
joblib.dump(vectorizer, MODEL_DIR / "tfidf_vectorizer.pkl")

print("\nModel saved successfully!")
