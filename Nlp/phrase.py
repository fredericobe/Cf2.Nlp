
import re
from param import Parameter
from corpusHelper import CorpusHelper
from corpusItem import CorpusItem
class Phrase:
    """A Phrase encapsulate a sentence string"""

    def __init__(self, sentence = None, intent = None, brain = None):
        self._entityToken = "__"
        self._entityNumberToken = "_"
        self._entityRegExPatterns = "{entity:{name:[a-zA-Z$_][a-zA-Z0-9$_]*}}"
        self._paramTypeRegExPattern = "[a-zA-Z]+" 
        self._entityNameRegExPatterns = "(?<=name:)[^}]*"
        self._reEngineEnt = re.compile(self._entityRegExPatterns)
        self._reEngineName = re.compile(self._entityNameRegExPatterns)
        self._sentence= sentence
        self._originalSentence = sentence #imutable sentence given from the user
        self.myIntent = intent
        self.myBraing = brain
        self.params = dict() 
        self._hasEntity = None

        self.Points = 0
        self.Corpus= []

    def _getTypeNameFromParam(self,term):
        match = re.search(self._paramTypeRegExPattern,term.stem)
        if match:
            return match.group(0)
        else:
            return None
            
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
        match= 0
        for item in corpus:
            if item.type == "entity":
                corpus = self.findCorpusByEntity(item.value)
            else:
                corpus = self.findCorpusByTerm(item.value)
            
            if corpus != None:
                match+= 1
           
        if match==0:
            return 0
        else:
            score = match/len(self.Corpus)
        return score

    def setIntent(self,intent):
        self.myIntent = intent

    def setSentence(self,sentence):
        self._sentence=sentence
        self._originalSentence=sentence
        self._hasEntity=None

    def getSentence(self):
        return self._sentence

    def hasEntity(self):
        if(self._hasEntity==None):
            self._hasEntity = len(self._reEngineEnt.findall(self._sentence))>0

        return self._hasEntity

    def resolveEntities(self):
        totalLength = len(self._sentence)
        match = self._reEngineEnt.search(self._sentence)
        i=1
        while(match!=None):
            end = match.end()
            start = match.start()
            value = match.group(0)
            name = self.getName(value)
            tempName = name + self._entityNumberToken + str(i)
            while( tempName in self.params):
                i = i +1
                tempName = name + self._entityNumberToken + str(i)

            param = Parameter()
            param.name = tempName
            param.type = name
            newSentence = self._sentence[0:start] + self._entityToken + tempName + self._entityToken + self._sentence[end:totalLength]
            self._sentence = newSentence
            self.params[tempName] = param
            match = self._reEngineEnt.search(self._sentence,start)

              #  ent.replace

    def getName(self, token):
        match =  self._reEngineName.search(token)
        return match.group(0)

    def resolve(self, wordProcess):
        totalPhrasePoints = 0

        if(self.hasEntity()):
              self.resolveEntities()

        sentence = self.getSentence()
        sentence = wordProcess.Tokenize(sentence)
        sentence = wordProcess.Stemming(sentence)
        sentence = wordProcess.RemoveStopWords(sentence)
        sentence = wordProcess.RemoveSpecialChars(sentence)
        helper = CorpusHelper()

        for word in sentence:
            if helper._isParam(word) == True:
                type = self._getTypeNameFromParam(word)
                corpus = self.findCorpusByEntity(type)
                if corpus == None:
                    corpus = CorpusItem()
                    corpus.type = "entity"
                    corpus.value = type
                    corpus.strength = 1
                    self.addCorpusItem(corpus)
                else:
                    corpus.strength +=1
                totalPhrasePoints = totalPhrasePoints + corpus.strength
            else:
                corpus = self.findCorpusByTerm(word)
                if corpus == None:
                    corpus = CorpusItem()
                    corpus.type = "term"
                    corpus.value = word
                    corpus.strength = 1
                    self.addCorpusItem(corpus)
                else:
                    corpus.strength +=1 
                totalPhrasePoints = totalPhrasePoints + corpus.strength
                
        self.Points = totalPhrasePoints
            