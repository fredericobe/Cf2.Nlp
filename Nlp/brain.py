from wordProcess import WordProcess
from corpusItem import CorpusItem
from sentence import Sentence
from corpusHelper import CorpusHelper
import re
from jsonConvert import JsonConvert


class Brain:


    def __init__(self, word, memory):

        self.wordProcess = word
        self.Memory = memory
        #self._reEngine = re.compile(self._paramNameAndOrderRegExPattern)
        self._currentContexts = []
        self.AccuracyFactor = 1 #Default value for intent selection
            
    def setMemory(self,memory):
        self.memory = memory
    
    def addCurrentContext(self, contextsList):
        """Add new contexts to the Brain"""
        self._currentContexts.extend(contextsList)
    
    def getCurrentContexts(self):
        """Get the list of current contexts to the Brain"""
        return self._currentContexts

    def clearContexts(self):
        self._currentContexts = []

    def Learn(self):
        for intent in self.Memory.GetIntents():
            intent.resolve(self.wordProcess)
        
        self.Memory.Save()
     

     

    def _getIntentsByContext(self):

        if len(self._currentContexts)==0:
            return list(filter(lambda x: len(x.InputContexts)==0 ,self.Memory.GetIntents()))              
        else:
            return list(filter(lambda x: len(x.InputContexts)>0 ,self.Memory.GetIntents())) 

    def GetMostProbableIntent(self,sentence):
        high_score = 0
        factor = 0
        selectedIntent = None
        selectedPhrase = None
        higherStrength = 0

        intentList = self._getIntentsByContext()
        procSentence = Sentence(self,sentence)
        for intent in intentList:
            result = self._getIntentScore(procSentence,intent)
            if (result['score']>high_score) or (result['score']==high_score and result['totalStrength']>higherStrength):
                high_score = result['score']
                higherStrength = result['totalStrength']
                selectedIntent = intent
                selectedPhrase = result
  
        if(selectedIntent!=None):
            if high_score>=self.AccuracyFactor:
                self.addCurrentContext(selectedIntent.OutputContexts)
            else:
                high_score = 0
                selectedIntent = None

        return {'intent':selectedIntent,'score': high_score, 'phrase': selectedPhrase}

    def _getIntentScore(self,processedSentece,intent):
        
        return intent.getPhraseByCorpus(processedSentece.Corpus)
        
   