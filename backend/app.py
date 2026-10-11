import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")


def ask_local_model(prompt: str) -> str:
    """Send a prompt to a locally running Ollama model."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=90,
    )
    response.raise_for_status()
    data = response.json()
    answer = data.get("response", "").strip()
    if not answer:
        raise RuntimeError("The local model returned an empty response.")
    return answer


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "model": OLLAMA_MODEL})


@app.post("/api/mission")
def mission():
    payload = request.get_json(silent=True) or {}
    interest = str(payload.get("interest", "nature")).strip()[:100]
    duration = str(payload.get("duration", "10 minutes")).strip()[:30]

    prompt = f"""
You are TrailMate, a friendly outdoor activity guide.
Create one safe, beginner-friendly outdoor nature mission about: {interest}.
The mission should take about {duration}, need no special equipment, and encourage
the person to put their phone away after reading it.
Return: a short title, 2-4 clear steps, and one reflection question.
Do not suggest eating or touching unknown plants, fungi, or animals.
Keep the response under 150 words.
"""
    try:
        return jsonify({"result": ask_local_model(prompt), "source": "local-model"})
    except requests.RequestException:
        return jsonify({
            "error": "Could not reach Ollama. Make sure Ollama is running and the model is downloaded.",
            "detail": "Start Ollama and run: ollama pull gemma3:1b",
        }), 503
    except (RuntimeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 502


@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()[:500]
    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    prompt = f"""
You are TrailMate, a beginner-friendly nature learning assistant.
Answer the user's question clearly and cautiously in under 180 words.
Never claim certainty when identifying a species from a text description.
Do not recommend eating wild plants or fungi or handling wildlife.
If relevant, suggest observing from a safe distance.
User question: {question}
"""
    try:
        return jsonify({"result": ask_local_model(prompt), "source": "local-model"})
    except requests.RequestException:
        return jsonify({
            "error": "Could not reach Ollama. Make sure Ollama is running and the model is downloaded."
        }), 503
    except (RuntimeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
