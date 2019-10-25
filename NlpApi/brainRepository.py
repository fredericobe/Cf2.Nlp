import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')

from brainEntity import BrainEntity
from pymongo import MongoClient
import mongoengine
from mongoengine import connect
import json
from jsonConvert import JsonConvert
from bson.objectid import ObjectId
from bson import json_util

class BrainRepository(object):
    
    def __init__(self, memoryId = None):
        self._mongo = MongoClient('localhost', 27017) 


    def addBrain(self, brain):
        id= str(self._mongo.memories.brains.insert_one(json.loads(JsonConvert.ToJSON(brain))).inserted_id)
        return id

    def updateBrain(self, id, brain):
        
        oId = None
        if isinstance(id,str):
            oId = ObjectId(id)
        else:
            oId = id
        
        if '_id' in brain.__dict__.keys():
            del brain._id

        self._mongo.memories.brains.update_one({'_id': oId}, {'$set': json.loads(JsonConvert.ToJSON(brain))})

    def getBrain(self, id):
        oId = None
        if isinstance(id,str):
            oId = ObjectId(id)
        else:
            oId = id

        brain = self._mongo.memories.brains.find_one({"_id": oId})
        brainJson = json.dumps(brain, sort_keys=True, indent=4, default=json_util.default)
        brainObj = JsonConvert.FromJSON(brainJson)
        brainObj._id = str(brainObj._id)
        return brainObj 

    def getBrains(self):
        
        brain = list(self._mongo.memories.brains.find({}))
        return brain
     