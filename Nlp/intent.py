from phrase import Phrase
from corpusItem import CorpusItem
from term import Term
from corpusHelper import CorpusHelper
from collections import deque

import random
from jsonConvert import JsonConvert

@JsonConvert.register
class Intent():
    """An Intent has a collection of Training Phrase, and possible responses."""
    helper = CorpusHelper()
    def __init__(self):
        self.Name = ""
        self._trainingPhrases = []
        self.Parameters = {}
        self.Responses = []
        self.Corpus = []
        self.InputContexts = []
        self.OutputContexts = []
        self.Completed = None #Identify if a intention if fully satisfied
        

    def addTrainingPhrase(self, sentence):
        """Get a simple sentece string and transform in the type Pharase, to add to the Phrase collection of the Intent"""
        phrase = Phrase(sentence)
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
        

    def getTrainingPhrases(self):
        return self._trainingPhrases;

    
    def resolve(self, wordProcess):
        self.Corpus = []
        for phrase in self.getTrainingPhrases():
            phrase.resolve(wordProcess)
            self.mergeEntities(phrase)

            for corpus in phrase.Corpus:
                self.addCorpusItem(corpus,True)


    def mergeEntities(self,phrase):
        """merge the entities of some phease into the Parameters of the Intent"""
        for param in phrase.params:
            if not param in self.Parameters:
                self.Parameters[param] = phrase.params[param]
    
    def addCorpusItem(self, corpusItem, merge = False):
        Intent.helper.addCorpusItem(self.Corpus,corpusItem,merge )

    def findCorpusByTerm(self,term):
        return Intent.helper.findCorpusByTerm(self.Corpus,term)

    def findCorpusByEntity(self,entityName):
        return Intent.helper.findCorpusByEntity(self.Corpus,entityName)
  

    def getPhraseByCorpus(self,corpus):
        ###Corpus is the corpus of the sentence that is being search
        score = 0
        selectedPhrase = None
        totalStrength = 0 
        for phrase in self.getTrainingPhrases():
            scoreAtual = phrase.getScoreByCorpus(corpus)
            if(scoreAtual > score):
                score =scoreAtual
                selectedPhrase = phrase
                totalStrength = phrase.TotalStrength 

        newCorpus = corpus.copy()
        self.Completed = True
        for paramName in self.Parameters:
            param = self.Parameters[paramName]
            item = Intent.helper.findCorpusByEntity(newCorpus ,param.type,True)
            if item!=None:
                param.actualValue = item.resolvedData['actual']
                param.resolvedValue = item.resolvedData['resolved']
            else:
                if param.mandatory:
                    self.Completed= False
        
        return {'phrase':selectedPhrase,'score': score, 'totalStrength' : totalStrength }
    

    def getResponse(self):


        if self.Completed:
            return random.choice(self.Responses)        
        else:
            for name in self.Parameters:
                param = self.Parameters[name]
                if param.mandatory and param.resolvedValue == None:
                    if len(param.fulfilmentPhrases) ==0:
                        return "What is " + name
                    else:
                        return random.choice(param.fulfilmentPhrases).sentence