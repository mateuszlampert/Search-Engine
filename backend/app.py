from flask import Flask, request, jsonify
from engine import Engine
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

engine: Engine = None

@app.route('/initialize', methods = ['POST'])
def initialize():
    if request.is_json:
        data = request.get_json()

        no_articles = int(data.get('no_articles'))
        svd = data.get('svd')
        idf = data.get('idf')

        print(svd)

        global engine

        if engine != None:
            if engine.no_articles != no_articles or engine.idf != idf or engine.svd != svd:
                engine = Engine(no_articles, svd, idf)
        else:
            engine = Engine(no_articles, svd, idf)

        response = {'status' : 'success'}

        return jsonify(response), 200

    else:
        response = {'status' : 'error'}

        return jsonify(response), 400

@app.route('/search', methods = {'POST'})
def search():
    global engine
    if engine == None:
        print("Engine have not been initialized yet. Creating engine with default parameters...")
        engine = Engine()

    if request.is_json:
        data = request.get_json()

        phrase = data.get('phrase')

        results = engine.search(phrase)

        return jsonify({'results' : results}), 200

    else:
        return jsonify({'status' : 'error'}), 400

if __name__ == '__main__':
    app.run(debug = True)