import requests

feedback_data = {
    "text": "Spending time with my family always fills me with joy and gratitude",
    "detected_emotion": "joy",
    "actual_emotion": "excited",
    "is_correct": True  
}

url = "http://127.0.0.1:5002/feedback"

try:
    response = requests.post(url, json=feedback_data)

    if response.status_code == 200:
        print("✅ Feedback saved successfully!")
    else:
        print(f"❌ Feedback could not be saved! HTTP Status: {response.status_code}")
        print("Yanıt:", response.text)
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to API server. Check if Flask is running.")
except requests.exceptions.RequestException as e:
    print(f"❌ An error occurred: {e}")
