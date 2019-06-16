#!flask/bin/python
from flask import render_template
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask import request

app = Flask(__name__)
mongo = PyMongo(app, uri =  "mongodb://localhost:27017/gustavorudiger")

@app.route('/')
def hello():
    return render_template('app.html')

@app.route('/api/v1.0/estudantes', methods=['GET'])
def get_estudantes():
    estudantes = mongo.db.estudantes
    output = []
    for e in estudantes.find():
        output.append({'nome' : e['nome '], 'ra' : e['ra']})
    #return jsonify({'estudantes': estudantes})
    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
