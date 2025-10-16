from flask import Flask, request, jsonify
import os


app =  Flask(__name__)

@app.post("/auth/verify")
def verify():
    data = request.get_json(silent=True) or {}
    token = data.get("id_token")
    
    if not token:
        return jsonify({"ok": False, "error": "id_token ausente!"}), 400
        
    return jsonify({"ok": True, "msg": "Token recebido com sucesso!"})


@app.route("/", methods=["GET"])
def raiz():
    return "online"

@app.route("/resposta", methods=["POST"])
def servidor():
    if not request.is_json:
        return jsonify(error="Envie JSON no corpo da requesição."), 400
    data = request.get_json(silent=True) or {}
    
    msg = data.get("msg", "Sem mensagem")
    
    if msg is None:
        return jsonify(error="Campo msg é obrigatório."), 400
        
    return jsonify(resposta=f"Recebi: {msg}")
    
    
if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
    
    
