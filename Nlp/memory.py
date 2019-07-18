from entities import Entity

from regExpEntity import RegExpEntity

import re

class Memory():
    """A Memory is the repository of the related Intents and Entities"""

    def __init__(self):
        self._intents= []
        self._entities= []


    def GetIntents(self):
        return self._intents

    def SetIntents(self, itens):
        self._intents = itens

    def GetEntities(self):
        return self._entities

    def SetEntities(self, itens):
        self._entities = itens

    def AddIntent(self, intent):
        self._intents.append(intent)

    def AddEntity(self, entity):
        self._entities.append(entity)

    def GetIntent(self, name):
        for intent in self.GetIntents():
            if intent.Name == name:
                return intent

        return None
    

    def GetEntity(self, name):
        for entity in self.GetEntities():
            if entity.Name == name:
                return entity

        return None

    def FindEntity(self, word):
        ###Lookup the given term into the momory of entities
        for entity in self.GetEntities():
            if isinstance(entity,Entity):
                result =  entity.GetSynonym(word)
                if result != None:
                    return result
            else:
               if isinstance(entity,RegExpEntity):
                   r = re.compile(entity.RegExp)
                   result = r.search(word)
                   if result != None:
                       return {'entity': entity, 'resolved': word, 'actual' : word}
                       return 

        return None
    
    def Save(self):
        #This method is suposed to be implemented in derived classes
        pass