from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Rota de teste
@app.route('/')
def home():
    return "ZapAgent IA está online e funcional!"

# Rota de resposta para o bot do WhatsApp
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
        "model": "nousresearch/deepseek-llama-3-8b",  # ou outro modelo gratuito que preferires
        "messages": [
            {"role": "user", "content": msg}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        resposta = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        resposta = f"Erro ao obter resposta da IA: {str(e)}"

    return jsonify({"resposta": resposta})

# Iniciar o servidor Flask no Replit
app.run(host='0.0.0.0', port=3000)
