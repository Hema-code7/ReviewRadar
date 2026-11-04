
import joblib

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_DIR = BASE_DIR / "models" / "saved"

model = joblib.load(MODEL_DIR / "review_classifier.pkl")
vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")


def detect_ai_review(review):

    review_tfidf = vectorizer.transform([review])

    prediction = model.predict(review_tfidf)[0]

    probability = model.predict_proba(review_tfidf)[0]

    if prediction == 1:
        result = "AI-generated"
        confidence = probability[1]
    else:
        result = "Human-written"
        confidence = probability[0]

    return {
        "prediction": result,
        "confidence": round(float(confidence), 4)
    }

