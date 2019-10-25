import sys

from flask import Flask, request
from flask_restful import Resource, Api,abort
from json import dumps
#from flask.ext.jsonpify import jsonify
sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')
app = Flask("NlpApi")
api = Api(app)

import json


from jsonConvert import JsonConvert
from bson.objectid import ObjectId
from bson import json_util
from brainRepository import BrainRepository

class BrainListApi(Resource):
    def __init__(self, brainRepository= None):

        if(brainRepository == None):
            self.brainRep = BrainRepository()
        else:
            self.brainRep = brainRepository
    
    def get(self):
            brains = self.brainRep.getBrains()
            return JsonConvert.ToJSON(brains)
                
    def post(self,payload = "" ):
        if payload=="":
            payload = request.json

        brain = JsonConvert.FromJSON(payload)
        ret = self.brainRep.addBrain(brain)
        return ret,201

class BrainItemApi(Resource):

    def __init__(self, brainRepository= None):

        if(brainRepository == None):
            self.brainRep = BrainRepository()
        else:
            self.brainRep = brainRepository
    
   
    def put(self,id,payload = ""):
        if payload=="":
            payload = request.json

        brain = JsonConvert.FromJSON(payload)
        ret = self.brainRep.updateBrain(id,brain)
        return id,200



    def get(self,id=0):
  
        brain = self.brainRep.getBrain(id)
        if(brain!=None):
            return JsonConvert.ToJSON(brain)
        else:
            abort(404, message='no brain was found')

api.add_resource(BrainListApi, '/brain') # Route_1
api.add_resource(BrainItemApi, '/brain/<id>') # Route_2

#api.add_resource(BrainApi, '/brain') # Route_1

if __name__ == '__main__':
     app.run(port='5002')