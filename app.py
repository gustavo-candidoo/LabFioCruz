from flask import Flask, request, jsonify
from models.db import professores 

app = Flask(__name__)

@app.route('/professores', methods=['GET'] )
def obter_prof():
    return jsonify(professores)

@app.route('/professores/<int:id>', methods=['GET'])
def consultar_prof_id(id):
    for professor in professores:
        if professor.get('id') == id:
            return jsonify(professor)
        
@app.route('/professores/<int:id>', methods=['PUT'])
def editar_prof_id(id):
    prof_alterado = request.get_json()
    for i, professor in enumerate(professores):
        if professor.get('id') == id:
            professores[i].update(prof_alterado)
            return jsonify(professores[i])
        
@app.route('/professores', methods=['POST'])
def novo_prof():
    novo_prof = request.get_json()
    professores.append(novo_prof)

    return jsonify(professores)

@app.route('/professores/<int:id>', methods=['DELETE'])
def excluir_prof(id):
    for i, professor in enumerate(professores):
        if professor.get('id') == id:
            del professores[i]

    return jsonify(professores)

app.run(port=5000, host='localhost', debug=True)