#!flask/bin/python
from flask import render_template
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask import request
from flask import make_response

app = Flask(__name__)
mongo = PyMongo(app, uri =  "mongodb://host.docker.internal:27017/gustavorudiger")
#mongo = PyMongo(app, uri =  "mongodb://127.0.0.1:27017/gustavorudiger")

def get_item(obj):
    return {
        'nome' : obj['nome'], 
        'idade_ate_31_12_2016' : obj['idade_ate_31_12_2016'], 
        'ra' : obj['ra'], 
        'campus' : obj['campus'], 
        'municipio' : obj['municipio'], 
        'curso' : obj['curso'],
        'modalidade' : obj['modalidade'],
        'nivel_do_curso' : obj['nivel_do_curso'],
        'data_inicio' : obj['data_inicio']
        }

@app.route('/')
def hello():
    return render_template('app.html')

@app.route('/api/v1.0/estudantes', methods=['GET'])
def get_estudantes():
    modalidade = request.args.get('modalidade', default = None)
    inicio = request.args.get('inicio', default = None)
    fim = request.args.get('fim', default = None)
    params = {}
    
    if(modalidade is not None):
        params['modalidade'] = modalidade
    
    if(inicio is not None and fim is not None):
        params['data_inicio'] = { '$gt': inicio, '$lt': fim } 
    elif(inicio is not None and fim is None):
        params['data_inicio'] = { '$gt': inicio }
    elif(inicio is None and fim is not None):
        params['data_inicio'] = { '$lt': fim }

    estudantes = mongo.db.estudantes.find(params).sort("_id", -1)
    output = []
    for e in estudantes:
        output.append(get_item(e))
    return jsonify({'result': output})

@app.route('/api/v1.0/cursos', methods=['GET'])
def get_cursos():
    campus = request.args.get('campus', default = None)
    params = {}
    
    if(campus is not None):
        params['campus'] = campus

    cursos = mongo.db.estudantes.distinct('curso', params)
    output = []
    for c in cursos:
        output.append(c)
    return jsonify({'result': output})

@app.route('/api/v1.0/total_alunos', methods=['GET'])
def get_total_alunos():    
    campus = request.args.get('campus', default = None)
    inicio = request.args.get('inicio', default = None)
    fim = request.args.get('fim', default = None)
    params = {}
    
    if(campus is not None):
        params['campus'] = campus
    if(inicio is not None and fim is not None):
        params['data_inicio'] = { '$gt': inicio, '$lt': fim } 
    elif(inicio is not None and fim is None):
        params['data_inicio'] = { '$gt': inicio }
    elif(inicio is None and fim is not None):
        params['data_inicio'] = { '$lt': fim }

    total_alunos = mongo.db.estudantes.find(params).count()
    output = total_alunos
    return jsonify({'result': output})

@app.route('/api/v1.0/aluno', methods=['POST'])
def add_aluno():
    estudantes = mongo.db.estudantes
    aluno = request.get_json()
    for prop in aluno:
        if( prop != 'municipio'):
            aluno[prop] = aluno[prop].upper()
    aluno_id = estudantes.insert(aluno)
    novo_aluno = estudantes.find_one({'_id': aluno_id })
    output = get_item(novo_aluno)
    return make_response( jsonify({'result' : output}), 201)

@app.route('/api/v1.0/aluno', methods=['DELETE'])
def delete_aluno():
    ra = request.args.get('ra', default = None)
    campus = request.args.get('campus', default = None)
    minimum_requirements = False
    params = {}
    
    if(ra is not None):
        params['ra'] = ra
        minimum_requirements = True
    
    if(minimum_requirements and campus is not None):
        params['campus'] = campus
    if(minimum_requirements):
        mongo.db.estudantes.delete_many(params)    

    return jsonify({'result': 'success'}) if minimum_requirements else jsonify({'error': 'O RA do aluno deve ser informado!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
