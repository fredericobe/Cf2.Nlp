from phrase import Phrase

class Intent:
    """An Intent has a collection of Training Phrase, and possible responses."""
    def __init__(self):
        self.Name = ""
        self._trainingPhrases = []
        self.Parameters = {}
        self.Responses = []
        self.Corpus= []
        self.InputContexts = []
        self.OutputContexts = []
        self.TotalPoints = 0

    def addTrainingPhrase(self, sentence):
        """Get a simple sentece string and transform in the type Pharase, to add to the Phrase collection of the Intent"""
        phrase = Phrase(sentence)
        phrase.setIntent(self)
        self._trainingPhrases.append(phrase);

    def addResponse(self, sentence):
        """Add a response sentence to this Intent"""
        self.Responses.append(sentence);
    
    def addOutputContext(self, sentence):
        """Add an output context to this intent. An output context is set when a intent is fulfilled"""
        self.OutputContexts.append(sentence);

    def addInputContext(self, sentence):
        """Add an input context to this intent. An input context is validated to a intent to be fulfilled"""
        self.InputContexts.append(sentence);
    
    def getHigherPointPhrase(self):
        """gets a phrase with the highest number of points"""
        higherPoint=0
        for phrase in self._trainingPhrases:
            if phrase.Points > higherPoint:
                higherPoint = phrase.Points
        return higherPoint
        
    def calculatePoints(self):
        totalPoints = 0 #keeps the current total of points of this intent, for future accuracy factor
        for x in self.Corpus:
            totalPoints = totalPoints + x.strength
        self.TotalPoints        = totalPoints

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