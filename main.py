from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Memória temporária e histórico por agente
memoria_agentes = {}    # { agent_id ou numero: última mensagem }
historico_agentes = {}  # { agent_id ou numero: [mensagens trocadas] }

@app.route('/')
def home():
    return "ZapAgent IA está online e funcional!"

# Teste GET simples (apenas mensagem)
@app.route('/responder', methods=['GET'])
def responder_get():
    msg = request.args.get('msg', '')
    if not msg:
        return jsonify({"resposta": "⚠️ Nenhuma mensagem recebida."})
    return gerar_resposta(msg)

# Teste POST simples (sem número)
@app.route('/responder', methods=['POST'])
def responder_post():
    data = request.get_json()
    msg = data.get('msg', '')
    prompt = data.get('prompt', 'Você é um agente inteligente de atendimento.')
    if not msg:
        return jsonify({"resposta": "⚠️ Nenhuma mensagem recebida."})
    return gerar_resposta(msg, prompt)

# POST com número e suporte a agent_id único (multi-agente)
@app.route('/responder/<numero>', methods=['POST'])
def responder_por_numero(numero):
    data = request.get_json()
    msg = data.get('msg', '')
    prompt = data.get('prompt', 'Você é um agente inteligente de atendimento.')
    agent_id = data.get('agent_id', numero)  # se não enviar agent_id, usar o número como fallback

    if not msg:
        return jsonify({"resposta": "⚠️ Nenhuma mensagem recebida."})

    # Salvar memória e histórico
    memoria_agentes[agent_id] = msg
    historico_agentes.setdefault(agent_id, []).append({"user": msg})

    resposta_obj = gerar_resposta(msg, prompt)
    resposta_data = resposta_obj.get_json()
    resposta_texto = resposta_data.get("resposta", "")
    historico_agentes[agent_id].append({"bot": resposta_texto})

    # Limitar histórico local (máx. 50 entradas)
    if len(historico_agentes[agent_id]) > 50:
        historico_agentes[agent_id] = historico_agentes[agent_id][-50:]

    return jsonify(resposta_data)

# Rota para obter status e histórico do agente
@app.route('/status/<numero>', methods=['GET'])
def status_agente(numero):
    agent_id = request.args.get('agent_id', numero)
    memoria = memoria_agentes.get(agent_id, '')
    historico = historico_agentes.get(agent_id, [])
    return jsonify({
        "numero": numero,
        "memoria_ultima_mensagem": memoria,
        "conversas": historico[-10:]
    })

# Função central de geração de resposta da IA via OpenRouter
def gerar_resposta(msg, prompt="Você é um agente inteligente de atendimento."):
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        return jsonify({"resposta": "❌ API KEY não configurada no servidor."}), 500

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

# Iniciar servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
