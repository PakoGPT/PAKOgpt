from flask import Flask, request, jsonify, render_template
import requests
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

@app.route("/")
def index():
    return render_template("chat-ui.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input_lt = data.get("message", "")

    # Išverčiam į anglų kalbą
    user_input_en = translator.translate(user_input_lt, dest='en').text

    # Siunčiam į Ollama
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": user_input_en,
        "stream": False
    })

    if response.ok:
        response_json = response.json()
        ai_text_en = response_json.get("response", "")
        # Verčiam atgal į lietuvių
        ai_text_lt = translator.translate(ai_text_en, dest='lt').text
        return jsonify({"response": ai_text_lt.strip()})

    return jsonify({"error": "Nepavyko gauti atsakymo iš Ollama"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
