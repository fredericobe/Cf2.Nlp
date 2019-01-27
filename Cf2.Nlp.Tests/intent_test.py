import unittest
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
        intent = Intent()
        intent.Name ="Falando de amor"
        corpus = CorpusItem()
        corpus.type = "term"
        corpus.value = "teste"
        corpus.strength = 1
        intent.addCorpusItem(corpus)
        corpusItem = intent.findCorpusByTerm("teste")
        self.assertEquals(corpusItem.strength,1)

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




if __name__ == '__main__':
    unittest.main()