from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Dados(Resource):
    def get(self):
        print(request.get_json())
        return jsonify({ 'data': 1 })

api.add_resource(Dados, '/')

if __name__ == '__main__':
    app.run(debug=True)