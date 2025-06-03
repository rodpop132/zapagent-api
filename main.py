from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "ZapAgent IA está online e funcional!"

# ✅ GET simples para testes
@app.route('/responder', methods=['GET'])
def responder_get():
    msg = request.args.get('msg', '')
    if not msg:
        return jsonify({"resposta": "⚠️ Nenhuma mensagem recebida."})
    return gerar_resposta(msg)

# ✅ POST simples para testes
@app.route('/responder', methods=['POST'])
def responder_post():
    data = request.get_json()
    msg = data.get('msg', '')
    prompt = data.get('prompt', 'Você é um agente inteligente de atendimento.')
    if not msg:
        return jsonify({"resposta": "⚠️ Nenhuma mensagem recebida."})
    return gerar_resposta(msg, prompt)

# ✅ POST por número (recomendado para múltiplos agentes)
@app.route('/responder/<numero>', methods=['POST'])
def responder_por_numero(numero):
    data = request.get_json()
    msg = data.get('msg', '')
    prompt = data.get('prompt', 'Você é um agente inteligente de atendimento.')
    if not msg:
        return jsonify({"resposta": "⚠️ Nenhuma mensagem recebida."})
    return gerar_resposta(msg, prompt)

# 🔁 Função compartilhada
def gerar_resposta(msg, prompt="Você é um agente inteligente de atendimento."):
    api_key = os.environ.get('OPENROUTER_API_KEY')

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://zapagent-ai-builder.lovable.app",
        "X-Title": "ZapAgent AI"
    }

    data = {
        "model": "nousresearch/deephermes-3-llama-3-8b-preview:free",
        "messages": [
            {"role": "system", "content": prompt},
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

# 🌐 Iniciar servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
