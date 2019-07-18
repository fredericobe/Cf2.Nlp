import re
from corpusHelper import CorpusHelper
class PhraseHelper:
    
    def __init__(self, sentence = None, intent = None, brain = None):
        self._entityToken = "__"
        self._entityNumberToken = "_"
        self._entityRegExPatterns = "{entity:{name:[a-zA-Z$_][a-zA-Z0-9$_]*}}"
        self._paramTypeRegExPattern = "[a-zA-Z]+" 
        self._entityNameRegExPatterns = "(?<=name:)[^}]*"
        self._reEngineEnt = re.compile(self._entityRegExPatterns)
        self._reEngineName = re.compile(self._entityNameRegExPatterns)
        self._corpus = CorpusHelper()

    def _getTypeNameFromParam(self,term):
        match = re.search(self._paramTypeRegExPattern,term.stem)
        if match:
            return match.group(0)
        else:
            return None

    def getName(self, token):
        match =  self._reEngineName.search(token)
        return match.group(0)