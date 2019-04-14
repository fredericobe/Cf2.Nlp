import nltk 
from nltk.stem import RSLPStemmer
from term import Term
class WordProcess:
    """WordProcess is low level class to pre process words, performing task as clearing stop words, stemming the words  and creating tokens from word"""
    def __init__(self):
        pass
    
    def Tokenize(self,sentence):
        sentence = sentence.lower()
        sentence = nltk.word_tokenize(sentence)
        return sentence

    def Stemming(self,wordArray):
        stemmer = RSLPStemmer()
        if(isinstance(wordArray, str)):
            term = Term()
            term.value = wordArray
            term.stem = stemmer.stem(wordArray.lower())
            return term
        else:
            phrase = []
            for word in wordArray:
                term = Term()
                term.value = word
                term.stem = stemmer.stem(word.lower())
                phrase.append(term)
            return phrase
    
    def RemoveStopWords(self, termArray):

        stopwords = nltk.corpus.stopwords.words('portuguese')
        #TODO: Rethink this
        #stopwords = ["a","as","o","os","de","da","do","das","dos"]
        phrase = []
        for word in termArray:
            if word.value not in stopwords:
                phrase.append(word)
        return phrase

    def RemoveSpecialChars(self, termArray):
        ##TODO: Should use something more dinamyc based on the language, as stopwords does
        chars = [",",".","?","!"]
        phrase = []
        for word in termArray:
            if word.value not in chars:
                phrase.append(word)
        return phrase

