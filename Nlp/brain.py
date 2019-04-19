from wordProcess import WordProcess
from corpusItem import CorpusItem
from sentence import Sentence
from corpusHelper import CorpusHelper
import re
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
        for intent in self.Memory.Intents:
            intent.Corpus = []
            for phrase in intent.getTrainingPhrases():
                self._learn(intent,phrase)
            intent.calculatePoints()
     

    def _learn(self, intent, phrase):

        phrase.resolve(self.wordProcess)
        intent.mergeEntities(phrase)

        for corpus in phrase.Corpus:
            intent.addCorpusItem(corpus,True)

     

    def _getIntentsByContext(self):

        if len(self._currentContexts)==0:
            return list(filter(lambda x: len(x.InputContexts)==0 ,self.Memory.Intents))              
        else:
            return list(filter(lambda x: len(x.InputContexts)>0 ,self.Memory.Intents)) 

    def GetMostProbableIntent(self,sentence):
        high_score = 0
        factor = 0
        selectedIntent = None
        selectedPhrase = None
        higherStrength = 0

        intentList = self._getIntentsByContext()

        for intent in intentList:
            result = self.getIntentScore(sentence,intent)
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

    def getIntentScore(self,sentence,intent):
        procSentence = Sentence(self,sentence)
        return intent.getPhraseByCorpus(procSentence.Corpus)
        
    #def CalculateIntentScore(self,sentence,intent):
    #    score = 0 
    #    procSentence = Sentence(self,sentence)

    #    intent.getPhraseByCorpus(procSentence)
    #    #TODO: Converter para procurar tudo na phrase e nao na intencao
    #    for item in procSentence.corpus:
    #        if item.type == "entity":
    #            corpus = intent.findCorpusByEntity(item.value)
    #            if corpus != None:
    #                score += corpus.strength
    #        else:
    #            corpus = intent.findCorpusByTerm(item.value)
    #            if corpus != None:
    #                score += corpus.strength

    #    return procSentence.points/score
    #def CalculateIntentScore(self,sentence,intent):
    #    score = 0 
    #    procSentence = Sentence(self,sentence)
    #    #TODO: Iterar no Corpus da Sentence e rever o bloco abaixo
    #    for word in sentence:
    #        entity =  self.Memory.FindEntity(word)
    #        if entity != None:
    #                corpus = intent.findCorpusByEntity(entity.Name)
    #                if corpus != None:
    #                    strength = corpus.strength
    #                    score += strength
    #        else:
    #            corpus = intent.findCorpusByTerm(word)
    #            if corpus != None:
    #                strength = corpus.strength
    #                score += strength

    #    return score

