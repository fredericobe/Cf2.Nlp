import sys

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
#from flask.ext.jsonpify import jsonify
sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')
app = Flask("NlpApi")
api = Api(app)

from jsonConvert import JsonConvert
from mongoRep import MongoRep

class BrainApi(Resource):
     def get(self):
        rep = MongoRep()
        brains = rep.getBrains()
        return JsonConvert.ToJSON(brains)
        

api.add_resource(BrainApi, '/brain') # Route_1
#api.add_resource(IntentApi, '/intent') # Route_2

if __name__ == '__main__':
     app.run(port='5002')