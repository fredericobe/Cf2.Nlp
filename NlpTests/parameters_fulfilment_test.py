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
from entities import Entity
from intent import Intent
from memory import Memory
from regExpEntity import RegExpEntity
from param import Parameter
from sentence import Sentence

class Test_parameters_fulfilment_test(unittest.TestCase):

    def setUp(self):
        word = WordProcess()

        self.memory = Memory()
        self.brain = Brain(word,self.memory)

        intent = Intent()
        intent.Name ="intent_pizza"
        intent.addTrainingPhrase("quero comprar uma pizza de {entity:{name:pizza}}")
        intent.addTrainingPhrase("quero comprar uma pizza")
       
        intent.addResponse("Sua pizza será entregue")
        
        self.memory.AddIntent(intent)


        entity = Entity()
        entity.Name = "pizza"
        sin = Synonym(word)
        sin.setPrincipal("calabreza")
        
        entity.Synonymous.append(sin)

        sin = Synonym(word)
        sin.setPrincipal("mussarela")
        
        entity.Synonymous.append(sin)
        self.memory.AddEntity(entity)

        param = Parameter()
        param.name = 'pizza_1'
        param.mandatory = True
        param.type = 'pizza'
        param.fulfilmentPhrases.append(Sentence(self.brain,"Qual pizza você quer?"))
        intent.Parameters['pizza_1'] = param

        self.brain = Brain(word,self.memory)
        self.brain.Learn()



    def test_if_intent_incomplete_returns_completed_properly(self):
        result = self.brain.GetMostProbableIntent("quero comprar uma pizza de calabreza")
        intent = result["intent"]
        self.assertEqual(intent.Parameters["pizza_1"].actualValue,"calabreza","actualValue nao bateu")
        self.assertTrue(intent.Completed,"Não retornou completed corretamente")
        self.assertEqual(intent.getResponse(),"Sua pizza será entregue","Não retornou complted corretamente")

    def test_if_intent_incomplete_returns_uncompleted_properly(self):
        result = self.brain.GetMostProbableIntent("quero comprar uma pizza")
        intent = result["intent"] 
        self.assertFalse(intent.Completed,"Não retornou complted corretamente")
        self.assertEqual(intent.getResponse(),"Qual pizza você quer?","Não retornou fullfilment corretamente")


if __name__ == '__main__':
    unittest.main()
