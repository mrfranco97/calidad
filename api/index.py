# api/index.py
from flask import Flask, request, Response, jsonify
import os
from openai import OpenAI
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Instancia del nuevo cliente de OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "API funcionando correctamente"}), 200

@app.route("/api/chat", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "")
    sender = request.form.get("From", "")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # También podés usar "gpt-3.5-turbo"
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Error con OpenAI:", e)
        print("🔑 CLAVE API:", os.environ.get("OPENAI_API_KEY"))
        reply = "Lo siento, ocurrió un error al procesar tu mensaje."

    # Crear respuesta TwiML
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

    return Response(twiml, mimetype="application/xml")
