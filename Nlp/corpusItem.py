from jsonConvert import JsonConvert

@JsonConvert.register
class CorpusItem:
    """Corpus Item represent an Item in the corpus of words maintained within a Intent """
    
    def __init__(self):
        self.type = "" #a entity or a simple term 
        self.value = ""#the name of the entity or the term
        self.paramName = "" #the ordinal name of the parameter
        self.strength = 0  #represent how important this CorpusItem is in the Intent
        self.resolvedData = None #when looking up for a sentence, keeps the resolved value of the sentence in the Entity



