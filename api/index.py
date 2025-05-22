# api/index.py
from flask import Flask, request, Response, jsonify
import os
import requests

app = Flask(__name__)

# Usamos OpenRouter en lugar de OpenAI
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"  # libre de cuota

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "API funcionando correctamente"}), 200

@app.route("/api/chat", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "")
    sender = request.form.get("From", "")

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": incoming_msg}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()

        reply = response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("❌ Error con OpenRouter:", e)
        reply = "Lo siento, ocurrió un error al procesar tu mensaje."

    # Formato TwiML (XML) para Twilio
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

    return Response(twiml, mimetype="application/xml")
