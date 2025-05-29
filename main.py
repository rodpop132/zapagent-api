from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "ZapAgent IA está online e funcional!"

@app.route('/responder', methods=['GET'])
def responder():
    msg = request.args.get('msg', '')
    if not msg:
        return jsonify({"resposta": "⚠️ Nenhuma mensagem recebida."})

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "user", "content": msg}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        resposta_data = response.json()
        if "choices" in resposta_data and len(resposta_data["choices"]) > 0:
            resposta_texto = resposta_data["choices"][0]["message"]["content"]
        else:
            resposta_texto = "❌ Erro: Resposta da IA está vazia."
    except Exception as e:
        resposta_texto = f"❌ Erro ao obter resposta da IA: {str(e)}"

    return jsonify({"resposta": resposta_texto})

# Inicia o servidor Flask
app.run(host='0.0.0.0', port=3000)
