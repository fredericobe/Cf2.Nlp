import unittest
import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')
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


    def testar_stemin(self):
        word = WordProcess()
        result = word.Stemming(self.pharseExpected)
        self.assertEquals([result[0].stem,result[1].stem,result[2].stem,result[3].stem],["eu", "gost", "de", "corr"])

    def testar_tokenizacao_data_completa(self):
        word = WordProcess()
        result = word.Tokenize("10 de janeiro de 2019")
        self.assertEquals(result[0],"10 de janeiro de 2019")

    def testar_tokenizacao_data_hora_completa(self):
        word = WordProcess()
        result = word.Tokenize("10 de janeiro de 2019, as 19:40")
        self.assertEquals(result[0],"10 de janeiro de 2019, as 19:40")

    def testar_tokenizacao_data_simples(self):
        word = WordProcess()
        result = word.Tokenize("19/11/2018")
        self.assertEquals(result[0],"19/11/2018")
 

    def testar_tokenizacao_http_com_texto(self):
        word = WordProcess()
        result = word.Tokenize("qual endereco é esse http://www.google.com.br")
        self.assertEquals(result[4],"http://www.google.com.br")
    
    def testar_tokenizacao_http(self):
        word = WordProcess()
        result = word.Tokenize("http://www.google.com.br")
        self.assertEquals(result[0],"http://www.google.com.br")

    def testar_tokenizacao_https(self):
        word = WordProcess()
        result = word.Tokenize("https://www.google.com.br")
        self.assertEquals(result[0],"https://www.google.com.br")
 
    def testar_tokenizacao_url_sem_http(self):
        word = WordProcess()
        result = word.Tokenize("www.google.com.br")
        self.assertEquals(result[0],"www.google.com.br")

    def testar_tokenizacao_email(self):
        word = WordProcess()
        result = word.Tokenize("teste@teste.com")
        self.assertEquals(result[0],"teste@teste.com")

    def testar_tokenizacao_email_com_texto(self):
        word = WordProcess()
        result = word.Tokenize("seleciona esse email teste@teste.com")
        self.assertEquals(result[3],"teste@teste.com")


    def testar_tokenizacao_diversos_emails(self):
        word = WordProcess()
        result = word.Tokenize("seleciona esse email teste@teste.com e tambem esse teste1@tes-te1.com ok ")
        self.assertEquals(result[3],"teste@teste.com")
        self.assertEquals(result[7],"teste1@tes-te1.com")

    def testar_tokenizacao_diversas_urls_e_email(self):
        word = WordProcess()
        result = word.Tokenize("qual esse endereco http://www.google.com.br e esse teste1@tes-te1.com e www.uol.com.br")
        self.assertEquals(result[3],"http://www.google.com.br")
        self.assertEquals(result[6],"teste1@tes-te1.com")
        self.assertEquals(result[8],"www.uol.com.br")

    def testar_stemin_email(self):
        word = WordProcess()
        result = word.Stemming("teste@teste.com")
        self.assertEquals(result.stem,"teste@teste.com")

    def testar_stemin_data_completa(self):
        word = WordProcess()
        result = word.Stemming("10 de janeiro de 2018")
        self.assertEquals(result.stem,"10 de janeiro de 2018")

    def testar_stemin_data_simples(self):
        word = WordProcess()
        result = word.Stemming("10/01/2019")
        self.assertEquals(result.stem,"10/01/2019")

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