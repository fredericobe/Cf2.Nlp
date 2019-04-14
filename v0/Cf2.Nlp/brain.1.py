from wordProcess import WordProcess
import re
class Brain_obsolete:

    memories = []
    def __init__(self, word):
        self.wordProcess = word


    def Learning(self,training_data):
        corpus_words = {}
        for data in training_data:
            sentence = data['sentence']
            sentence = self.wordProcess.Tokenize(sentence)
            sentence = self.wordProcess.Stemming(sentence)
            sentence = self.wordProcess.RemoveStopWords(sentence)
            class_name = data['class']
            if class_name not in list(corpus_words.keys()):
                corpus_words[class_name] = {}
            for word in sentence:
                if word not in list(corpus_words[class_name].keys()):
                    corpus_words[class_name][word] = 1
                else:
                    corpus_words[class_name][word] += 1
        return corpus_words

        

    def calculate_score(self,sentence,corpus):
        high_score = 0
        classname = 'default'
        for wordClass in corpus.keys():
            score = 0
            score = self.calculate_class_score(sentence,wordClass,corpus)
            if score > high_score:
                high_score = score
                classname = wordClass
            
        return {'className':classname,'score': high_score}

    def calculate_class_score(self,sentence,class_name,corpus):
        score = 0 
        sentence = self.wordProcess.Tokenize(sentence)
        sentence = self.wordProcess.Stemming(sentence)
        for word in sentence:
            if word in corpus[class_name]:
                score += corpus[class_name][word]
        return score

