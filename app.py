import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)
client = genai.Client()

TIV_SYSTEM_PROMPT = (
    "You are 'Uncle Joe AI,' a friendly, knowledgeable, and culturally respectful AI assistant. "
    "Your primary language of communication is the Tiv language. You must understand and respond "
    "accurately using proper Tiv grammar, cultural idioms, and respectful vocabulary."
)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Missing message body"}), 400
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=data['message'],
            config=types.GenerateContentConfig(system_instruction=TIV_SYSTEM_PROMPT),
        )
        return jsonify({"status": "success", "reply": response.text.strip()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
