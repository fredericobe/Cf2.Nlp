import unittest
import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')
from brain import Brain
from wordProcess import WordProcess
from synonym import Synonym
from term import Term
from brain import Brain
from entities import Entity
from intent import Intent
from memory import Memory
from corpusItem import CorpusItem

class TestIntent(unittest.TestCase):

    def setUp(self):
        pass


    def testar_findCorpusByTerm(self):
        wp = WordProcess()
        intent = Intent()
        intent.Name ="Falando de amor"
        corpus = CorpusItem()
        corpus.type = "term"
        corpus.value = wp.Stemming("teste")
        corpus.strength = 1
        intent.addCorpusItem(corpus)
        
        term = wp.Stemming("teste")
        corpusItem = intent.findCorpusByTerm(term)
        self.assertEquals(corpusItem.strength,1)
   
    def testar_findCorpusByTermStrength2(self):
        wp = WordProcess()
        intent = Intent()
        intent.Name ="Falando de amor"
        corpus = CorpusItem()
        corpus.type = "term"
        corpus.value = wp.Stemming("teste")
        corpus.strength = 1
        intent.addCorpusItem(corpus)
        corpus = CorpusItem()
        corpus.type = "term"
        corpus.value = wp.Stemming("teste")
        corpus.strength = 1
        intent.addCorpusItem(corpus,True)
        
        terms = wp.Stemming("teste")
        corpusItem = intent.findCorpusByTerm(terms)
        self.assertEquals(corpusItem.strength,2)

    def testar_findCorpusByEntity(self):
        intent = Intent()
        intent.Name ="Falando de amor"
        corpus = CorpusItem()
        corpus.type = "entity"
        corpus.value = "teste"
        corpus.strength = 1
        intent.addCorpusItem(corpus)
        corpusItem = intent.findCorpusByEntity("teste")
        self.assertEquals(corpusItem.strength,1)

    def testar_randonResponse(self):
        intent = Intent()
        intent.Completed= True
        intent.addResponse("Resposta 1")
        intent.addResponse("Resposta 2")
        intent.addResponse("Resposta 3")

        response1 = intent.getResponse()
        response2 = intent.getResponse()
        response3 = intent.getResponse()

        self.assertTrue(response1 != response2 or response3 != response2 or response1 != response3)





if __name__ == '__main__':
    unittest.main()