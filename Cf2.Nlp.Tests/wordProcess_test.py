import unittest
from wordProcess import WordProcess
class WordProcessTest(unittest.TestCase):

    def setUp(self):
        self.pharse="Eu gosto de correr"
        self.pharseExpected=["eu","gosto", "de", "correr"]
        self.phraseParam = "Eu gosto de __fruta__"
        self.phraseParamExpected = ["eu","gosto","de", "__fruta__"]

    def testar_tokenizacao(self):
        word = WordProcess()
        result = word.Tokenize(self.pharse)
        self.assertEquals(result,self.pharseExpected)

    def testar_tokenizacao_param(self):
        word = WordProcess()
        result = word.Tokenize(self.phraseParam)
        self.assertEquals(result,self.phraseParamExpected)

    def testar_stemin(self):
        word = WordProcess()
        result = word.Stemming(self.pharseExpected)
        self.assertEquals([result[0].stem,result[1].stem,result[2].stem,result[3].stem],["eu", "gost", "de", "corr"])

    def testar_stemin_param(self):
        word = WordProcess()
        result = word.Stemming(self.phraseParamExpected) 
        self.assertEquals([result[0].stem,result[1].stem,result[2].stem,"__fruta__"],["eu", "gost", "de", "__fruta__"])

    def testar_stopWord(self):
        word = WordProcess()
        result = word.RemoveStopWords(word.Stemming(self.pharseExpected) )
        self.assertEquals([result[0].value,result[1].value],[ "gosto", "correr"])

    

if __name__ == '__main__':
    unittest.main()