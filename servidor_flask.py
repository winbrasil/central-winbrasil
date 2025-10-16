from flask import Flask, request, jsonify
import os
import requests

app =  Flask(__name__)

@app.post("/auth/verify")
def verificar_token():
    data = request.get_json(silent=True) or {}
    token = data.get("id_token")
    
    if not token:
        return jsonify({"ok": False, "error": "id_token ausente!"}), 400
        
    FIREBASE_API_KEY = "AIzaSyATicQTeRmBrWIHmNIzoi5zL3w-Lo7PkAw"
    
    url = f"https://identitytoolkit.google.apis.com/v1/accounts: lookup?key={FIREBASE_API_KEY}"
    
    try:
        resp = requests.post(url, json={"idToken": token})
        info = resp.json()
        
        if "users" in info:
            usuario = info["users"][0]
            email = usuario.get("email")
            uid = usuario.get("localId")
            
            return jsonify({"ok": True, "uid": uid, "email": email, "msg": "Token Válido!"})
            
        else:
            return jsonify({"ok": False, "error": "Token inválido ou expirado!", "detalhes": info}), 401
            
            
        
    except Exception as erro:
        return jsonify({"ok": False, "error": str(erro)}), 500
    
    
    


@app.route("/", methods=["GET"])
def home():
    return "servidor online"

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
    
    
