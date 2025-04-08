import gradio as gr
import requests
import matplotlib.pyplot as plt
from langdetect import detect




API_URL = "http://127.0.0.1:5002/predict"
FEEDBACK_URL = "http://127.0.0.1:5002/feedback"

# Emotions mapping with emojis
emotions_mapping = {
     "LABEL_0": "😍 Admiration", "LABEL_1": "😂 Amusement", "LABEL_2": "😡 Anger",
    "LABEL_3": "😤 Annoyance", "LABEL_4": "👍 Approval", "LABEL_5": "🤗 Caring",
    "LABEL_6": "😕 Confusion", "LABEL_7": "🤔 Curiosity", "LABEL_8": "😋 Desire",
    "LABEL_9": "😞 Disappointment", "LABEL_10": "👎 Disapproval",
    "LABEL_11": "🤢 Disgust", "LABEL_12": "😳 Embarrassment", "LABEL_13": "🤩 Excitement",
    "LABEL_14": "😨 Fear", "LABEL_15": "🙏 Gratitude", "LABEL_16": "😭 Grief", 
    "LABEL_17": "😊 Joy", "LABEL_18": "❤️ Love", "LABEL_19": "😰 Nervousness",
    "LABEL_20": "🌞 Optimism", "LABEL_21": "😌 Pride", "LABEL_22": "💡 Realization",
    "LABEL_23": "😅 Relief", "LABEL_24": "😔 Remorse", "LABEL_25": "😢 Sadness",
    "LABEL_26": "😲 Surprise", "LABEL_27": "😐 Neutral"
}

def analyze_sentiment(text):
    try:
        response = requests.post(API_URL, json={"text": text})
        response.raise_for_status()
        result = response.json()

        # Get top 3 emotions
        top_results = sorted(result, key=lambda x: x['score'], reverse=True)[:3]
        emotions = [emotions_mapping.get(res['emotion'], res['emotion']) for res in top_results]
        scores = [res['score'] for res in top_results]
        detected_language = top_results[0]['detected_language']

        # Create horizontal bar chart
        plt.figure(figsize=(8, 4))
        plt.barh(emotions, scores, color='skyblue')
        plt.xlabel("Score")
        plt.title("Top 3 Sentiments")
        plt.gca().invert_yaxis()
        plt.tight_layout()

        analysis_output = "\n".join(
            [f"{emotions[i]} - Score: {scores[i]:.4f} (Lang: {detected_language})" for i in range(len(top_results))]
        )

        return analysis_output, detected_language, plt
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", None, None

def submit_feedback(text, detected_emotion, feedback_correct, actual_emotion):
    if feedback_correct == "Evet":
        actual_emotion = detected_emotion

    feedback_data = {
        "text": text,
        "detected_emotion": detected_emotion,
        "actual_emotion": actual_emotion,
        "is_correct": feedback_correct == "Evet"
    }
    try:
        response = requests.post(FEEDBACK_URL, json=feedback_data)
        response.raise_for_status()
        return "Your feedback has been saved successfully!"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

with gr.Blocks() as app:
    gr.Markdown("# Sentiment Analysis and Feedback")
    text_input = gr.Textbox(label="Enter Text")
    submit_button = gr.Button("Analyze")

    output_text = gr.Textbox(label="Analysis Result")
    lang_output = gr.Textbox(label="Detected Language")
    chart_output = gr.Plot(label="Sentiment Chart")

    feedback_correct = gr.Radio(["Evet", "Hayır"], label="Is the result correct?")
    actual_emotion = gr.Dropdown(choices=list(emotions_mapping.values()), label="Select Correct Emotion")
    feedback_button = gr.Button("Submit Feedback")
    feedback_output = gr.Textbox(label="Feedback Status")

    def analyze_and_show_feedback(text):
        result, detected_lang, chart = analyze_sentiment(text)
        return result, detected_lang, chart

    submit_button.click(analyze_and_show_feedback, inputs=text_input, outputs=[output_text, lang_output, chart_output])
    feedback_button.click(submit_feedback, inputs=[text_input, output_text, feedback_correct, actual_emotion], outputs=feedback_output)

app.launch()
