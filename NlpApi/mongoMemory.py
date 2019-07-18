import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')

from memory import Memory
from pymongo import MongoClient
import mongoengine
from mongoengine import connect
import json
from jsonConvert import JsonConvert
from bson import BSON
from bson import json_util

@JsonConvert.register
class MongoMemory(Memory):
    
    def __init__(self, memoryId = None):
        self._id = memoryId
        self._cliente = MongoClient('localhost', 27017)
        #connect('memories')
        self._memories = self._cliente.memories
        if(self._id!=None):
            self._memory = self._memories.memory.find_one({"_id": self._id})
            ##TODO: If has id but don t find any memory, should throw an exception 
            self._id = self._memory['_id']
            memJson = json.dumps(self._memory, sort_keys=True, indent=4, default=json_util.default)
            menObj = JsonConvert.FromJSON(memJson)
            self._intents = menObj.Intents
            self._entities = menObj.Entities
        else:
            self._intents = []
            self._entities = []

    def GetIntents(self):
        return self._intents

    def SetIntents(self, itens):
        self._intents = itens
        self.__saveState()

    def GetEntities(self):
        return self._entities

    def SetEntities(self, itens):
        self._entities = itens
        self.__saveState()

    def AddIntent(self, intent):
        self._intents.append(intent)
        self.__saveState()

    def AddEntity(self, entity):
        self._entities.append(entity)
        self.__saveState()


    def Save(self):
        self.__saveState()

    def __saveState(self):
        value = tempMemoryIn(self._intents,self._entities)
        if(self._id == None):
            #doc = tempMemory()
            #doc.intents = self._intents
            #doc.entities =  self._entities
            #doc.save()
            
            id = self._memories.memory.insert_one(json.loads(JsonConvert.ToJSON(value))).inserted_id
            self._id = id
        else:
            self._memories.memory.update_one({'_id': self._id}, {'$set': json.loads(JsonConvert.ToJSON(value))})

@JsonConvert.register
class tempMemoryIn():

    def __init__(self, intents = [], entities = []):
        self.Intents = intents
        self.Entities = entities

@JsonConvert.register
class tempMemoryOut():
    
    def __init__(self,intents = [], entities = []):
        self.Intents = intents
        self.Entities = entities
        self._id = None

    