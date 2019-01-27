from wordProcess import WordProcess
from term import Term
class Synonym:
    """A Synonym is a way to determine different word related to the same meaning in a given context or system wide"""

    _principal = Term()
    _others = []

    def __init__(self, word):
        self.wordProcess = word

  

    def _getTerm(self,term):
        t = Term()
        t.value = term
        t.stem = self.wordProcess.Stemming([term])
        return t

    def setPrincipal(self,term):
        self._principal = self._getTerm(term)
  
    
    def getPrincipal(self):
        return self._principal

    def addOther(self, term):
        self._others.append(self._getTerm(term))

    def getOthers(self):
        return self._others

    
    def isSynonym(self,term):
        t = self._getTerm(term)

        if t.stem == self._principal.stem:
            return True

        for item in self._others:
            if item.stem == t.stem:
                return True

        return False
        