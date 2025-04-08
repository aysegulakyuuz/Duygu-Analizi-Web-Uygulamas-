from flask import Flask, request, jsonify
from transformers import pipeline
import sqlite3
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Load the model (ensure it's locally available)
try:
    classifier = pipeline("text-classification", model="./emotion_recognition_model", tokenizer="./emotion_recognition_model", return_all_scores=True)
except Exception as e:
    print("Error loading model:", e)
    exit()

DB_NAME = 'feedback.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            detected_emotion TEXT NOT NULL,
            actual_emotion TEXT,
            is_correct BOOLEAN NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return "Welcome to the Sentiment Analysis API! Use /predict endpoint to analyze text."


from langdetect import detect

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    detected_lang = detect(text)  # Metnin dilini algıla
    translated_text = GoogleTranslator(source='auto', target='en').translate(text)
    results = classifier(translated_text)

    top_results = sorted(results[0], key=lambda x: x['score'], reverse=True)[:3]

    formatted_result = [
        {
            "emotion": result["label"],
            "score": round(result["score"], 4),
            "detected_language": detected_lang  # Algılanan dil kodunu ekle
        }
        for result in top_results
    ]

    return jsonify(formatted_result)


@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    text = data.get("text")
    detected_emotion = data.get("detected_emotion")
    actual_emotion = data.get("actual_emotion")
    is_correct = data.get("is_correct")

    if not all([text, detected_emotion, actual_emotion, is_correct is not None]):
        return jsonify({"error": "Missing data"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (text, detected_emotion, actual_emotion, is_correct) VALUES (?, ?, ?, ?)",
                   (text, detected_emotion, actual_emotion, is_correct))
    conn.commit()
    conn.close()

    return jsonify({"message": "Feedback saved successfully!"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
