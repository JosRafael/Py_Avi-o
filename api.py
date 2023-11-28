from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/aviator/resultados')
def aviator_resultados():
    try:
        with open('resultados.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"erro": "Arquivo não encontrado"})

if __name__ == '__main__':
    app.run(debug=True)
