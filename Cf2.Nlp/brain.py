from wordProcess import WordProcess
from corpusItem import CorpusItem
import re
class Brain:


    def __init__(self, word, memory):
        self._entityRegExPatterns = "{entity:{name:[a-zA-Z$_][a-zA-Z0-9$_]*}}"
        self._paramNameAndOrderRegExPattern = "(\_\_[a-zA-Z]+\_\d\_\_)" ##matches __asdasd_2__ at the begining
        self._paramTypeRegExPattern = "[a-zA-Z]+" 
        self.wordProcess = word
        self.Memory = memory
        self._reEngine = re.compile(self._paramNameAndOrderRegExPattern)


    def setMemory(self,memory):
        self.memory = memory

    def Learn(self):
        for intent in self.Memory.Intents:
            for phrase in intent.getTrainingPhrases():
                if(not phrase.hasEntity()):
                    self._learnNoEntity(intent,phrase)
                else:
                    self._learnWithEntity(intent,phrase)
     
    def _isParam(self,term):
        match = re.match(self._paramNameAndOrderRegExPattern,term)
        if match:
            return True
        else:
            return False

    def _getTypeNameFromParam(self,term):
        match = re.search(self._paramTypeRegExPattern,term)
        if match:
            return match.group(0)
        else:
            return None
            
    def _learnNoEntity(self, intent, phrase):
        sentence = phrase.getSentence()
        sentence = self.wordProcess.Tokenize(sentence)
        sentence = self.wordProcess.Stemming(sentence)
        sentence = self.wordProcess.RemoveStopWords(sentence)
        for word in sentence:
            if self._isParam(word) == True:
                type = self._getTypeNameFromParam(word)
                corpus = intent.findCorpusByEntity(type)
                ##TODO: Need Refactoring in this part, to avoid repeting both if corpus == None: block
                if corpus == None:
                    corpus = CorpusItem()
                    corpus.type = "entity"
                    corpus.value = type
                    corpus.strength = 1
                    intent.addCorpusItem(corpus)
                else:
                    corpus.strength +=1
            else:
                corpus = intent.findCorpusByTerm(word)
                if corpus == None:
                    corpus = CorpusItem()
                    corpus.type = "term"
                    corpus.value = word
                    corpus.strength = 1
                    intent.addCorpusItem(corpus)
                else:
                    corpus.strength +=1 

    def _learnWithEntity(self, intent, phrase):
        phrase.resolveEntities()
        intent.mergeEntities(phrase)
        self._learnNoEntity(intent,phrase)
        #TODO: Retirar o learnNoEntity e fazer um learning onde a entidade no corpus seja só o tipo


    def GetMostProbableIntent(self,sentence):
        high_score = 0
        selectedIntent = None
        for intent in self.Memory.Intents:
            score = 0
            score = self.CalculateIntentScore(sentence,intent)
            if score > high_score:
                high_score = score
                selectedIntent = intent
            
        return {'intent':selectedIntent,'score': high_score}

    def CalculateIntentScore(self,sentence,intent):
        score = 0 
        sentence = self.wordProcess.Tokenize(sentence)
        sentence = self.wordProcess.Stemming(sentence)
        sentence = self.wordProcess.RemoveStopWords(sentence)
        for word in sentence:
            entity =  self.Memory.FindEntity(word)
            if entity != None:
                    corpus = intent.findCorpusByEntity(entity.Name)
                    if corpus != None:
                        strength = corpus.strength
                        score += strength
            else:
                corpus = intent.findCorpusByTerm(word)
                if corpus != None:
                    strength = corpus.strength
                    score += strength

        return score

