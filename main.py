from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ ZapAgent IA está online!"

@app.route('/responder', methods=['GET'])
def responder():
    msg = request.args.get('msg', '')
    if not msg:
        return jsonify({"resposta": "⚠️ Nenhuma mensagem recebida."})

    # API KEY segura nas variáveis de ambiente do Render
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return jsonify({"resposta": "❌ Chave de API não encontrada."})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://zapagent-ai-builder.lovable.app",  # ou a página onde está o frontend
        "X-Title": "ZapAgent IA"
    }

    data = {
        "model": "nousresearch/deephermes-3-llama-3-8b-preview:free",
        "messages": [
            {"role": "user", "content": msg}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        resposta_data = response.json()
        resposta_texto = resposta_data["choices"][0]["message"]["content"]
    except Exception as e:
        resposta_texto = f"❌ Erro ao obter resposta da IA: {str(e)}"

    return jsonify({"resposta": resposta_texto})

# Iniciar servidor Flask
if __name__ == "__main__":
    print("✅ Endpoint de verificação simples")
    app.run(host='0.0.0.0', port=3000)
