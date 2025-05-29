# ------------------------
# ✅ main.py (API em Flask)
# ------------------------

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Simulador de "banco de dados" de prompts personalizados
PROMPTS = {}

@app.route('/')
def home():
    return "ZapAgent IA está online e funcional!"

# Endpoint para salvar prompt personalizado por número
@app.route('/set_prompt', methods=['POST'])
def set_prompt():
    data = request.get_json()
    numero = data.get('numero')
    prompt = data.get('prompt')

    if not numero or not prompt:
        return jsonify({"erro": "Número e prompt são obrigatórios."}), 400

    PROMPTS[numero] = prompt
    return jsonify({"mensagem": "✅ Prompt salvo com sucesso!"})

# Endpoint para responder mensagens
@app.route('/responder', methods=['GET'])
def responder():
    msg = request.args.get('msg', '')
    numero = request.args.get('numero', '')
    prompt_base = PROMPTS.get(numero, '')

    if not msg:
        return jsonify({"resposta": "⚠️ Nenhuma mensagem recebida."})

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": prompt_base},
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

# Inicia o servidor Flask no Replit ou Render
app.run(host='0.0.0.0', port=3000)
