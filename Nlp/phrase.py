
import re
from param import Parameter
from corpusHelper import CorpusHelper
from corpusItem import CorpusItem
from phraseHelper import PhraseHelper
from jsonConvert import JsonConvert

@JsonConvert.register
class Phrase():
    """A Phrase encapsulate a sentence string"""

    def __init__(self, sentence = None, intent = None ):
    
        self._sentence= sentence
        self._originalSentence = sentence #imutable sentence given from the user
        self.params = dict() 
        self._hasEntity = None
        self.TotalStrength  = 0
        self.Corpus= []

            
    def addCorpusItem(self, corpus):
        self.Corpus.append(corpus)

    def findCorpusByTerm(self,term):
        for item in self.Corpus:
                if item.type == "term" and item.value.stem==term.stem:
                    return item

        return None

    def findCorpusByEntity(self,entityName):
        for item in self.Corpus:
                if item.type == "entity" and item.value==entityName:
                    return item

        return None
    
    def getScoreByCorpus(self, corpus):
        helper = PhraseHelper()
        match= 0
        found = None
        newPhraseCorpus = self.Corpus.copy()
        for item in corpus:
            if item.type == "entity":
                found= helper._corpus.findCorpusByEntity(newPhraseCorpus,item.value)
            else:
                found = helper._corpus.findCorpusByTerm(newPhraseCorpus,item.value)
            
            if found != None:
                del newPhraseCorpus[newPhraseCorpus.index(found)]
                match+= 1
            
            
        if match==0:
            return 0
        else:
            score = match/len(self.Corpus)
        return score



    def setSentence(self,sentence):
        self._sentence=sentence
        self._originalSentence=sentence
        self._hasEntity=None

    def getSentence(self):
        return self._sentence

    def hasEntity(self):
        if(self._hasEntity==None):
            helper = PhraseHelper()
            self._hasEntity = len(helper._reEngineEnt.findall(self._sentence))>0

        return self._hasEntity

    def resolveEntities(self):
        helper = PhraseHelper()
        totalLength = len(self._sentence)
        match = helper._reEngineEnt.search(self._sentence)
        i=1
        while(match!=None):
            end = match.end()
            start = match.start()
            value = match.group(0)
            name = helper.getName(value)
            tempName = name + helper._entityNumberToken + str(i)
            while( tempName in self.params):
                i = i +1
                tempName = name + helper._entityNumberToken + str(i)

            param = Parameter()
            param.name = tempName
            param.type = name
            newSentence = self._sentence[0:start] + helper._entityToken + tempName + helper._entityToken + self._sentence[end:totalLength]
            self._sentence = newSentence
            self.params[tempName] = param
            match = helper._reEngineEnt.search(self._sentence,start)

              #  ent.replace


    def resolve(self, wordProcess):
        

        if(self.hasEntity()):
              self.resolveEntities()

        sentence = self.getSentence()
        sentence = wordProcess.Tokenize(sentence)
        sentence = wordProcess.Stemming(sentence)
        sentence = wordProcess.RemoveStopWords(sentence)
        sentence = wordProcess.RemoveSpecialChars(sentence)
        helper = PhraseHelper()

        for word in sentence:
            if helper._corpus._isParam(word) == True:
                type = helper._getTypeNameFromParam(word)
                #corpus = self.findCorpusByEntity(type)
                #if corpus == None:
                corpus = CorpusItem()
                corpus.type = "entity"
                corpus.value = type
                corpus.strength = 1
                self.addCorpusItem(corpus)
                #else:
                 #   corpus.strength +=1
            else:
                #corpus = self.findCorpusByTerm(word)
                #if corpus == None:
                    corpus = CorpusItem()
                    corpus.type = "term"
                    corpus.value = word
                    corpus.strength = 1
                    self.addCorpusItem(corpus)
               # else:
                #    corpus.strength +=1 
                
        self.TotalStrength = 0
        for corpus in self.Corpus:
            self.TotalStrength += corpus.strength
         
            