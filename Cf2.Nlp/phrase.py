import re
from param import Parameter
class Phrase:
    """A Phrase encapsulate a sentence string"""

    def __init__(self, sentence = None, intent = None, brain = None):
        self._entityToken = "__"
        self._entityNumberToken = "_"
        self._entityRegExPatterns = "{entity:{name:[a-zA-Z$_][a-zA-Z0-9$_]*}}"
        self._entityNameRegExPatterns = "(?<=name:)[^}]*"
        self._reEngineEnt = re.compile(self._entityRegExPatterns)
        self._reEngineName = re.compile(self._entityNameRegExPatterns)
        self._sentence= sentence
        self._originalSentence = sentence #imutable sentence given from the user
        self.myIntent = intent
        self.myBraing = brain
        self.params = dict() 
        self._hasEntity = None

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

            

