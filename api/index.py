# api/index.py
from flask import Flask, request, Response
import os
import openai
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Clave de API de OpenAI desde variables de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "")
    sender = request.form.get("From", "")

    # Llamada a OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "Lo siento, ocurrió un error al procesar tu mensaje."

    # Crear XML de respuesta para Twilio
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

    return Response(twiml, mimetype="application/xml")
