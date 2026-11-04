import pandas as pd
import joblib

from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


# Project paths
BASE_DIR = Path(__file__).resolve().parents[3]

DATASET_DIR = BASE_DIR / "dataset" / "processed"
MODEL_DIR = BASE_DIR / "backend" / "models" / "saved"
OUTPUT_DIR = BASE_DIR / "backend" / "models" / "saved"

# Load test dataset
test_df = pd.read_parquet(DATASET_DIR / "test_processed.parquet")

X_test = test_df["review_text"]
y_test = test_df["label"]


# Load trained model and vectorizer
model = joblib.load(MODEL_DIR / "review_classifier.pkl")
vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")


# Transform test reviews
X_test_tfidf = vectorizer.transform(X_test)


# Make predictions
predictions = model.predict(X_test_tfidf)


# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)

print("\nFinal Test Results")
print("------------------")
print("Accuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    target_names=["Human-written", "AI-generated"]
))


# Generate confusion matrix
cm = confusion_matrix(y_test, predictions)

print("\nConfusion Matrix:")
print(cm)


# Save confusion matrix image
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Human-written", "AI-generated"]
)

display.plot()
plt.title("ReviewRadar - Confusion Matrix")
plt.savefig(OUTPUT_DIR / "confusion_matrix.png", bbox_inches="tight")

print("\nConfusion matrix saved successfully!")
