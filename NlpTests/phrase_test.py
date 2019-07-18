import unittest
import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')
from wordProcess import WordProcess
from synonym import Synonym
from term import Term
from entities import Entity
from intent import Intent
from memory import Memory
from phrase import Phrase
from brain import Brain
class TestPhrase(unittest.TestCase):

    def setUp(self):
        self.memoryComplex = Memory()
        entity = Entity()
        entity.Name = "mineral"
        word = WordProcess()
        self.brain = Brain(word,self.memoryComplex)
        sin = Synonym(word)
        sin.setPrincipal("pedra")
        sin.addOther("pedregulho")
        sin.addOther("cascalho")
        sin.addOther("ROCHA")

        entity.Synonymous.append(sin)

        sin = Synonym(word)
        sin.setPrincipal("metal")
        sin.addOther("ouro")
        sin.addOther("prata")
        sin.addOther("bronze")

        entity.Synonymous.append(sin)
        self.memoryComplex.AddEntity(entity)


    def testarHasEntities(self):
        phrase = Phrase("qual a intenção de {entity:{name:mineral}}")
        self.assertTrue(phrase.hasEntity())

    def testarHasNoEntities(self):
        phrase = Phrase("eu te amo")
        self.assertFalse(phrase.hasEntity())



    def testarGetAllEntity(self):
        phrase = Phrase("qual a intenção de {entity:{name:mineral}} e {entity:{name:animal}}")
        phrase.resolveEntities()
        
        self.assertEqual(len(phrase.params),2,"Total de parametros nao bate")
        self.assertEqual(phrase.params["mineral_1"].type,"mineral","tipo nao bate")
        self.assertEqual(phrase.params["animal_1"].type,"animal","tipo 2 nao bate")

    def testarGetAllEntitySameType(self):
        phrase = Phrase("qual a intenção de {entity:{name:animal}} e {entity:{name:animal}}")
        phrase.resolveEntities()
        self.assertEqual(len(phrase.params),2,"Total de parametros nao bate")
        self.assertEqual(phrase.params["animal_1"].type,"animal","tipo nao bate")
        self.assertEqual(phrase.params["animal_2"].type,"animal","tipo 2 nao bate")

    def testarGetSingleEntity(self):
        phrase = Phrase("qual a intenção de {entity:{name:mineral}}")
        phrase.resolveEntities()
        self.assertEqual(len(phrase.params),1,"Total de parametros nao bate")
        self.assertEqual(phrase.params["mineral_1"].type,"mineral","tipo nao bate")
    
    def testResolveEntities(self):
        phrase = Phrase("qual a intenção de {entity:{name:mineral}}",None)
        phrase.resolveEntities()
        self.assertEqual(phrase.getSentence(),"qual a intenção de __mineral_1__")
 
    def testResolveMultipleEntitiesOfSameType(self):
        phrase = Phrase("qual a intenção de {entity:{name:mineral}} e {entity:{name:mineral}}")
        phrase.resolveEntities()
        self.assertEqual(phrase.getSentence(),"qual a intenção de __mineral_1__ e __mineral_2__")

    def testResolveMultipleEntitiesOfDifferentType(self):
        phrase = Phrase("qual a intenção de {entity:{name:mineral}} e {entity:{name:animal}}")
        phrase.resolveEntities()
        self.assertEqual(phrase.getSentence(),"qual a intenção de __mineral_1__ e __animal_1__")

    #def testgetScoreByCorpus(self):
        
    #    memorySimple = Memory()
    #    intent = Intent()
    #    intent.Name ="medo"
    #    intent.addTrainingPhrase("estou com medo")
    #    intent.addTrainingPhrase("tenho medo de fantasma")
    #    memorySimple.Intents.append(intent)

        

    #    #self.expectedCorpusMedo = {'est': 1, 'med': 2, 'tenh': 1, 'fantasm': 1}
    #    self.expectedCorpusMedo = { 'med': 2, 'fantasm': 1}

if __name__ == '__main__':
    unittest.main()
