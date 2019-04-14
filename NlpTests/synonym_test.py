import unittest
import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')
from wordProcess import WordProcess
from synonym import Synonym
from term import Term

class TestSynonym(unittest.TestCase):

    def setUp(self):
        pass

    def testar_isSinonym_pedra(self):
        word = WordProcess()
        synonym = Synonym(word)
        
        
        synonym.setPrincipal("pedra")
        synonym.addOther("rocha")
        synonym.addOther("cascalho")

        self.assertTrue(synonym.isSynonym("PEDRA"))
    
    def testar_isSinonym_cascalho(self):
        word = WordProcess()
        synonym = Synonym(word)
        
        
        synonym.setPrincipal("pedra")
        synonym.addOther("rocha")
        synonym.addOther("cascalho")

        self.assertTrue(synonym.isSynonym("cascalhos"))   

    def testar_isSinonym_pedregulho(self):
        word = WordProcess()
        synonym1 = Synonym(word)
        
        
        synonym1.setPrincipal("pedra")
        synonym1.addOther("rocha")
        synonym1.addOther("cascalho")
        self.assertFalse(synonym1.isSynonym("pedregulho"))       


if __name__ == '__main__':
    unittest.main()