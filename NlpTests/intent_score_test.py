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
class Test_intent_score(unittest.TestCase):

    def setUp(self):
        
        word = WordProcess()
        self.memory = Memory()
        
        intent = Intent()
        intent.Name ="pedras"
        intent.addTrainingPhrase("seleção de {entity:{name:mineral}}")
        intent.addTrainingPhrase("uma {entity:{name:mineral}} é um mineral")
       
        intent.addResponse("Mineral escolhido")
        
        self.memory.Intents.append(intent)

        word = WordProcess()

        entity = Entity()
        entity.Name = "mineral"
        word = WordProcess()
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
        self.memory.Entities.append(entity)

        self.brain = Brain(word,self.memory)
        self.brain.Learn()

    
        
        

if __name__ == '__main__':
    unittest.main()
