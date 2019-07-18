from synonym import Synonym
from jsonConvert import JsonConvert

@JsonConvert.register
class Entity():
    """An Entity is a component to combine multiple Synonym with a common objective"""
    def __init__(self):
        self.Name = ""
        self.Synonymous = []

    def GetSynonym(self,word):
        for synonym in self.Synonymous:
            if synonym.isSynonym(word):
                return {'entity': self, 'resolved': synonym.getPrincipal().value, 'actual' : word}

        
        return None
            