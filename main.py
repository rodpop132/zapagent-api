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
        "model": "nousresearch/deepseek-llama-3-8b",
        "messages": [
            {"role": "user", "content": msg}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        data = response.json()

        resposta = data.get("choices", [{}])[0].get("message", {}).get("content", None)

        if not resposta:
            raise Exception("Resposta vazia da IA.")

        return jsonify({"resposta": resposta})

    except Exception as e:
        return jsonify({"resposta": f"❌ Erro ao obter resposta da IA: {str(e)}"})

app.run(host='0.0.0.0', port=3000)
