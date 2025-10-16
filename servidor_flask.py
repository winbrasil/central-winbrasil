from flask import Flask, request, jsonify


app =  Flask(__name__)

@app.route("/resposta", methods=["POST"])
def servidor():
    dados = request.get_json()
    
    msg = dados.get()
    
    #resposta = ""
    print(msg)
    
    return jsonify(200)
    
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=True)