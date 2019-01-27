class Memory:
    """A Memory is the repository of the related Intents and Entities"""

    def __init__(self):
        self.Intents= []
        self.Entities= []

    def GetIntent(self, name):
        for intent in self.Intents:
            if intent.Name == name:
                return intent

        return None
    

    def GetEntity(self, name):
        for entity in self.Entities:
            if entity.Name == name:
                return entity

        return None

    def FindEntity(self, term):
        ###Lookup the given term into the momory of entities
        for entity in self.Entities:
            if entity.HasSynonym(term):
                return entity

        return None