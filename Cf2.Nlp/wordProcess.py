import nltk 
from nltk.stem import RSLPStemmer

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
        phrase = []
        for word in wordArray:
            phrase.append(stemmer.stem(word.lower()))
        return phrase
    
    def RemoveStopWords(self, wordArray):
        stopwords = nltk.corpus.stopwords.words('portuguese')
        phrase = []
        for word in wordArray:
            if word not in stopwords:
                phrase.append(word)
        return phrase

    def RemoveSpecialChars(self, wordArray):
        ##TODO: Should use something more dinamyc based on the language, as stopwords does
        chars = [",",".","?","!"]
        phrase = []
        for word in wordArray:
            if word not in chars:
                phrase.append(word)
        return phrase

