import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')

from memory import Memory
from brainEntity import BrainEntity
from pymongo import MongoClient
import mongoengine
from mongoengine import connect
import json
from jsonConvert import JsonConvert
from bson import BSON
from bson import json_util

from brain import Brain

class NlpService(object):
    
    def postBrain(self, name, language, accuracyFactor):
        brain = BrainEntity()
        brain.Name = name
        brain.Language = language
        brain.AccuracyFactor = accuracyFactor

    def createSession(self, brainId,clientId):


    def request(self,brainId,sessionId,query):

        



