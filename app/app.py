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
    params = {}
    
    if(modalidade is not None):
        params['modalidade'] = modalidade
    
    if(inicio is not None):
        params['data_inicio'] = { '$gt': inicio }

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
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
