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
from brain import Brain
from wordProcess import WordProcess
from synonym import Synonym
from term import Term
from entities import Entity
from intent import Intent

class mongo_brain_context_test(unittest.TestCase):


    
    def setUp(self):
        
        word = WordProcess()

        self.memory = MongoMemory()
      
        
        intent = Intent()
        intent.Name ="Boas_Vindas"
        intent.addTrainingPhrase("Olá, tudo bem?")
        intent.addTrainingPhrase("Oi, como vai?")
        intent.addTrainingPhrase("eae, tudo bem?")
        intent.addResponse("Olá, vou bem e você?")
        intent.addResponse("Estou ótimo, obrigado por perguntar!")

        self.memory.AddIntent(intent)

        intent = Intent()
        intent.Name ="comprar"
        intent.addTrainingPhrase("Gostaria de fazer uma compra")
        intent.addTrainingPhrase("quero comprar uma coisa")
        intent.addTrainingPhrase("quero fazer uma compra")
        intent.addOutputContext("compra")
        intent.addResponse("Certo, o que você gostaria de comprar?")
        
        self.memory.AddIntent(intent)


        intent = Intent()
        intent.Name ="compra_fim"
        intent.addTrainingPhrase("quero comprar uma bicicleta")
        intent.addTrainingPhrase("quero comprar um eletrodoméstico")
        intent.addInputContext("compra")
        intent.addOutputContext("fim_compra")
        intent.addResponse("Certo, entendi o que você quer comprar. Obrigado")
        
        self.memory.AddIntent(intent)

        word = WordProcess()
        brain = Brain(word,self.memory)
        
        brain.Learn()
        self.id = self.memory._id

    def testar_boas_vindas_sem_contexto(self):
        
        mem = MongoMemory(self.id)
        word = WordProcess()
        brain = Brain(word,mem)
        
        
        result = brain.GetMostProbableIntent("Olá, tudo bem?")
        self.assertEqual(result["intent"].Name,"Boas_Vindas","Nome do Intent não bateu")
        self.assertEqual(mem._id,self.id)

    def testar_boas_vindas_com_contexto(self):
        mem = MongoMemory(self.id)
        word = WordProcess()
        brain = Brain(word,mem)
        brain.addCurrentContext("any")
        result = brain.GetMostProbableIntent("Olá, tudo bem?")
        self.assertEqual(result["intent"],None,"Não era para encontrar Intent, mas achou")
        self.assertEqual(mem._id,self.id)


    def testar_comprar_com_contexto_sucesso(self):
        mem = MongoMemory(self.id)
        word = WordProcess()
        brain = Brain(word,mem)

        result = brain.GetMostProbableIntent("quero fazer uma compra")
        self.assertEqual(result["intent"].Name,"comprar","nao achou a primeira intent de comprar")
        self.assertEqual(len(brain.getCurrentContexts()),1,"nao definiu o contexto")
        self.assertEqual(brain.getCurrentContexts()[0],"compra","nao definiu o contexto")
       
        result = brain.GetMostProbableIntent("quero comprar um eletrodoméstico")
        self.assertEqual(result["intent"].Name,"compra_fim","nao achou a segunda intent de comprar")
        self.assertEqual(len(brain.getCurrentContexts()),2,"nao definiu o contexto")
        self.assertEqual(brain.getCurrentContexts()[0],"compra","nao definiu o contexto compra")
        self.assertEqual(brain.getCurrentContexts()[1],"fim_compra","nao definiu o contexto fim_compra")
        self.assertEqual(mem._id,self.id)

    def testar_comprar_segundo_nivel_sem_contexto_falha(self):
        mem = MongoMemory(self.id)
        word = WordProcess()
        brain = Brain(word,mem)
        result = brain.GetMostProbableIntent("quero comprar um eletrodoméstico")
        self.assertEqual(result["intent"],None,"nao deveria achar um Intent mas achou")
        self.assertEqual(mem._id,self.id)

if __name__ == '__main__':
    unittest.main()
