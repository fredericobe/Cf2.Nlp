
import unittest
import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('NlpApi')
sys.path.append('/NlpApi')
sys.path.append('../NlpApi')
sys.path.append('../')


from mongoMemory import MongoMemory
from brainEntity import BrainEntity
from brainRepository import BrainRepository

class Test_mongo_brain_crud_test(unittest.TestCase):
    
    def setUp(self):
        pass
        

    def testar_adicionar_cerebro(self):
        brain = BrainEntity()
        brain.Name = "My Brain"
        brain.Language = "pt-BR"
        brain.AccuracyFactor = 1

        rep = BrainRepository()
        id = rep.addBrain(brain)

        self.assertIsNotNone(id,"Id = "+id)

    def testar_obter_cebebro(self):
        
        brain = BrainEntity()
        brain.Name = "My Brain"
        brain.Language = "pt-BR"
        brain.AccuracyFactor = 1

        rep = BrainRepository()
        id = rep.addBrain(brain)

        brain = rep.getBrain(id)

        self.assertEqual(str(brain._id),id)

    def testar_obter_lista_cebebro(self):
        
        brain = BrainEntity()
        brain.Name = "My Brain List 1"
        brain.Language = "pt-BR"
        brain.AccuracyFactor = 1

        rep = BrainRepository()
        id = rep.addBrain(brain)

        brain = BrainEntity()
        brain.Name = "My Brain List 2"
        brain.Language = "pt-BR"
        brain.AccuracyFactor = 1
        id = rep.addBrain(brain)

        list = rep.getBrains()
        self.assertGreater(len(list),1)

    def testar_atualizar_cebebro(self):
        
        brain = BrainEntity()
        brain.Name = "My Brain"
        brain.Language = "pt-BR"
        brain.AccuracyFactor = 1

        rep = BrainRepository()
        id = rep.addBrain(brain)

        brain1 = rep.getBrain(id)

        brain1.Name = "My Brain Update"

        rep.updateBrain(id,brain1)

        brain2 = rep.getBrain(id)

        self.assertEqual(brain2._id,id)
        self.assertEqual(brain2.Name,"My Brain Update")

