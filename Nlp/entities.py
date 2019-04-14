from synonym import Synonym
class Entity:
    """An Entity is a component to combine multiple Synonym with a common objective"""
    def __init__(self):
        self.Name = ""
        self.Synonymous = []

    def HasSynonym(self,word):
        for synonym in self.Synonymous:
            if synonym.isSynonym(word):
                return True
            else:
                return False
            