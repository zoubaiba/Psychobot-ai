"""
Lightweight Flask API — replaces Django for standalone deployment.
Endpoints mirror the original Django views without requiring
Supabase authentication or a PostgreSQL database.
"""
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os, sys

load_dotenv()

# Mock Django settings
class MockSettings:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

sys.modules.setdefault('django.conf', type(sys)('django.conf'))
sys.modules['django.conf'].settings = MockSettings()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services import (
    compute_burnout_score,
    chat_with_gemini,
    update_score_from_chat,
    determine_level,
    build_context_prefix,
    detect_besoins_ressources,
)

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": "llama-3.3-70b-versatile"})


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Compute burn-out risk score from questionnaire responses.
    Body: { "responses": { "question": "answer", ... } }
    """
    data      = request.get_json()
    responses = data.get("responses", {})

    if not responses:
        return jsonify({"error": "responses field is required"}), 400

    result = compute_burnout_score(responses)
    level  = determine_level(result["score"])

    return jsonify({
        "score":  result["score"],
        "level":  level,
        "signals": result["raisons"],
    })


@app.route("/chat", methods=["POST"])
def chat():
    """
    Send a message to PsychoBot with conversation history.
    Body: {
        "message": "...",
        "history": [{"role": "user"|"assistant", "content": "..."}],
        "score": 0-100  (optional, for resource detection)
    }
    """
    data     = request.get_json()
    message  = data.get("message", "")
    history  = data.get("history", [])
    score    = data.get("score", 0)

    if not message:
        return jsonify({"error": "message field is required"}), 400

    response = chat_with_gemini(history, message)

    updated_history = history + [
        {"role": "user",      "content": message},
        {"role": "assistant", "content": response},
    ]
    needs = detect_besoins_ressources(updated_history, score)

    return jsonify({
        "response":            response,
        "resource_category":   needs.get("categorie"),
        "urgent":              needs.get("urgence", False),
        "redirect_message":    needs.get("message_redirection"),
    })


@app.route("/session/close", methods=["POST"])
def close_session():
    """
    Refine the burn-out score after a complete chat session.
    Body: {
        "history": [...],
        "initial_score": 0-100,
        "initial_signals": [...]
    }
    """
    data            = request.get_json()
    history         = data.get("history", [])
    initial_score   = data.get("initial_score", 0)
    initial_signals = data.get("initial_signals", [])

    updated = update_score_from_chat(history, initial_score, initial_signals)
    level   = determine_level(updated["score"])

    return jsonify({
        "final_score":   updated["score"],
        "final_level":   level,
        "final_signals": updated["raisons"],
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)