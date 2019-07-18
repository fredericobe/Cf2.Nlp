from corpusItem import CorpusItem
from corpusHelper import CorpusHelper
from jsonConvert import JsonConvert

@JsonConvert.register
class Sentence():
    """Represents the user input"""

    def __init__(self, brain = None, sentence = None):
        self.sentence = sentence
        self.brain = brain 
        self.Corpus = []
        self.points = 0
        helper = CorpusHelper()
        self.processedSentence = ""
        if(brain!=None):
            
            self.processedSentence = brain.wordProcess.Tokenize(sentence)
            self.processedSentence = brain.wordProcess.Stemming(self.processedSentence)
            self.processedSentence = brain.wordProcess.RemoveStopWords(self.processedSentence)
            self.processedSentence = brain.wordProcess.RemoveSpecialChars(self.processedSentence)

            for term in self.processedSentence:
                corpus = CorpusItem()
                entity =  brain.Memory.FindEntity(term.value)
                if entity != None:
                    corpus.type = "entity"
                    corpus.strength = 1  
                    corpus.value = entity['entity'].Name
                    corpus.resolvedData = {'resolved' : entity['resolved'], 'actual' : entity['actual']}
                else:
                    corpus.type = "term"
                    corpus.value = term
                    corpus.strength = 1  
                helper.addCorpusItem(self.Corpus,corpus)
            
            