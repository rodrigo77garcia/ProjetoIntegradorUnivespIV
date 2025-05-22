from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

bp_chat = Blueprint('chat', __name__)
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

@bp_chat.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")

    if not TOGETHER_API_KEY:
        return jsonify({"error": "TOGETHER_API_KEY não está configurada."}), 500

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data, timeout=10)
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({"response": reply})
    except requests.exceptions.Timeout:
        return jsonify({"error": "A requisição excedeu o tempo limite."}), 504

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Erro de conexão com a API externa."}), 502

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro na requisição: {str(e)}"}), 500

    except (KeyError, IndexError):
        return jsonify({"error": "Erro ao processar a resposta da API."}), 500
