import requests

url = "http://127.0.0.1:5002/predict"

# Test cümleleri
test_cases = [
    "I am feeling fantastic today!",
    "I am so sad and lonely.",
    "This is a neutral statement.",
    "I am really angry right now!",
    "Je suis très heureux aujourd'hui",  # Fransızca
    "Estoy muy feliz hoy",                # İspanyolca
    "Bu proje çok heyecan verici!",        # Türkçe
    "Ich bin glücklich"                    # Almanca
]

# Her metni test et
for text in test_cases:
    data = {"text": text}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        print(f"Input: {text}")
        print(f"Detected Language: {result[0]['detected_language']}")
        for item in result:
            print(f"Emotion: {item['emotion']}, Score: {item['score']:.4f}")
        print("-" * 50)
    else:
        print(f"API Hatası: {response.status_code}, Mesaj: {response.text}")
