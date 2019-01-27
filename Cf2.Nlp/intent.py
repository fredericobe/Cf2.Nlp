from phrase import Phrase

class Intent:
    """An Intent has a collection of Training Phrase, and possible responses."""
    def __init__(self):
        self.Name = ""
        self._trainingPhrases = []
        self.Parameters = {}
        self.Responses = []
        self.Corpus= []
    
    def addTrainingPhrase(self, sentence):
        """Get a simple sentece string and transform in the type Pharase, to add to the Phrase collection of the Intent"""
        phrase = Phrase(sentence)
        phrase.setIntent(self)
        self._trainingPhrases.append(phrase);

    def getTrainingPhrases(self):
        return self._trainingPhrases;

    def mergeEntities(self,phrase):
        """merge the entities of some phease into the Parameters of the Intent"""
        for param in phrase.params:
            if not param in self.Parameters:
                self.Parameters[param] = phrase.params[param]
    
    def addCorpusItem(self, corpus):
        self.Corpus.append(corpus)

    def findCorpusByTerm(self,term):
        for item in self.Corpus:
                if item.type == "term" and item.value==term:
                    return item

        return None

    def findCorpusByEntity(self,entityName):
        for item in self.Corpus:
                if item.type == "entity" and item.value==entityName:
                    return item

        return None