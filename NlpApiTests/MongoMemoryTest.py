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
from intent import Intent

class Test_memory_mongo_test(unittest.TestCase):

    def setUp(self):
        pass
        

    def testar_gravacao_nova_memoria_uma_intecao(self):
        memory = MongoMemory()
        
        
        intent = Intent()
        intent.Name ="Boas_Vindas"
        intent.addTrainingPhrase("Olá, tudo bem?")
        intent.addTrainingPhrase("Oi, como vai?")
        intent.addTrainingPhrase("eae, tudo bem?")
        intent.addResponse("Olá, vou bem e você?")
        intent.addResponse("Estou ótimo, obrigado por perguntar!")

        memory.AddIntent(intent)

        self.assertFalse(memory._id == None)
        self.assertEqual(len(memory.GetIntents()),1)

    def testar_gravacao_nova_memoria_uma_intecao_depois_outra_com_outra_memoria(self):
        memory = MongoMemory()
        
        
        intent = Intent()
        intent.Name ="Boas_Vindas"
        intent.addTrainingPhrase("Olá, tudo bem?")
        intent.addTrainingPhrase("Oi, como vai?")
        intent.addTrainingPhrase("eae, tudo bem?")
        intent.addResponse("Olá, vou bem e você?")
        intent.addResponse("Estou ótimo, obrigado por perguntar!")

        memory.AddIntent(intent)

        id = memory._id 

        memory2 = MongoMemory(id)
        intent = Intent()
        intent.Name ="comprar"
        intent.addTrainingPhrase("Gostaria de fazer uma compra")
        intent.addTrainingPhrase("quero comprar uma coisa")
        intent.addTrainingPhrase("quero fazer uma compra")
        intent.addOutputContext("compra")
        intent.addResponse("Certo, o que você gostaria de comprar?")
        
        memory2.AddIntent(intent)

        id2= memory2._id

        self.assertEqual(len(memory2.GetIntents()),2)
        self.assertEqual(id2,id)



    def testar__nova_memoria_duas_intencoes(self):
        memory = MongoMemory()
        
        
        intent = Intent()
        intent.Name ="Boas_Vindas"
        intent.addTrainingPhrase("Olá, tudo bem?")
        intent.addTrainingPhrase("Oi, como vai?")
        intent.addTrainingPhrase("eae, tudo bem?")
        intent.addResponse("Olá, vou bem e você?")
        intent.addResponse("Estou ótimo, obrigado por perguntar!")

        memory.AddIntent(intent)

        id = memory._id 

        intent = Intent()
        intent.Name ="comprar"
        intent.addTrainingPhrase("Gostaria de fazer uma compra")
        intent.addTrainingPhrase("quero comprar uma coisa")
        intent.addTrainingPhrase("quero fazer uma compra")
        intent.addOutputContext("compra")
        intent.addResponse("Certo, o que você gostaria de comprar?")
        
        memory.AddIntent(intent)

        id2= memory._id

        self.assertEqual(len(memory.GetIntents()),2)
        self.assertEqual(id2,id)

if __name__ == '__main__':
    unittest.main()