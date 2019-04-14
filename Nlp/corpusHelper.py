from corpusItem import CorpusItem   
from term import Term    
import re
class CorpusHelper:


    
    def __init__(self):
        self._entityRegExPatterns = "{entity:{name:[a-zA-Z$_][a-zA-Z0-9$_]*}}"
        self._paramNameAndOrderRegExPattern = "(\_\_[a-zA-Z]+\_\d\_\_)" ##matches __asdasd_2__ at the begining
        

    def _mergeCorpusItem(self, corpusA,corpusB):
        """merge a corpusItem (corusB) into a existim corpusItem (corpusA). If corpusA is None, it will be created. The result will be returned from the method"""
        if corpusA == None:
            corpusA = CorpusItem()
            corpusA.paramName = corpusB.paramName
            corpusA.strength = corpusB.strength
            corpusA.type = corpusB.type
            corpusA.value = corpusB.value
            corpusA.resolvedData = corpusB.resolvedData 
        else:
            corpusA.strength = corpusA.strength + corpusB.strength

        return corpusA
    
    def addCorpusItem(self, corpus, corpusItem):
        c = None
        if corpusItem.type == "term":
            c = self.findCorpusByTerm(corpus,corpusItem.value)
        else:
            c = self.findCorpusByEntity(corpus,corpusItem.value)
        
        found = c != None
        c = self._mergeCorpusItem(c,corpusItem)

        if found:
            for n, i in enumerate(corpus):
                if i.type == corpusItem.type and i.value == corpusItem.value:
                    corpus[n] = c
        else:
            corpus.append(c)

    def findCorpusByTerm(self,corpus,term):
        for item in corpus:
                if item.type == "term" and item.value.stem==term.stem:
                    return item

        return None

    def findCorpusByEntity(self,corpus,entityName):
        for item in corpus:
                if item.type == "entity" and item.value==entityName:
                    return item

        return None
    
    def _isParam(self,term):
        if(isinstance(term, str)):
            match = re.match(self._paramNameAndOrderRegExPattern,term)
        else:
            match = re.match(self._paramNameAndOrderRegExPattern,term.value)
        if match:
            return True
        else:
            return False