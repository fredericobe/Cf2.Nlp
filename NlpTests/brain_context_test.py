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
class Test_brain_context_test(unittest.TestCase):


    def setUp(self):
        
        word = WordProcess()

        self.memory = Memory()
      
        
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
        self.brain = Brain(word,self.memory)
        
        self.brain.Learn()

    def testar_boas_vindas_sem_contexto(self):
        result = self.brain.GetMostProbableIntent("Olá, tudo bem?")
        self.assertEqual(result["intent"].Name,"Boas_Vindas","Nome do Intent não bateu")

    def testar_boas_vindas_com_contexto(self):
        self.brain.addCurrentContext("any")
        result = self.brain.GetMostProbableIntent("Olá, tudo bem?")
        self.assertEqual(result["intent"],None,"Não era para encontrar Intent, mas achou")

    def testar_comprar_com_contexto_sucesso(self):
        self.brain.clearContexts()
        result = self.brain.GetMostProbableIntent("quero fazer uma compra")
        self.assertEqual(result["intent"].Name,"comprar","nao achou a primeira intent de comprar")
        self.assertEqual(len(self.brain.getCurrentContexts()),1,"nao definiu o contexto")
        self.assertEqual(self.brain.getCurrentContexts()[0],"compra","nao definiu o contexto")
       
        result = self.brain.GetMostProbableIntent("quero comprar um eletrodoméstico")
        self.assertEqual(result["intent"].Name,"compra_fim","nao achou a segunda intent de comprar")
        self.assertEqual(len(self.brain.getCurrentContexts()),2,"nao definiu o contexto")
        self.assertEqual(self.brain.getCurrentContexts()[0],"compra","nao definiu o contexto compra")
        self.assertEqual(self.brain.getCurrentContexts()[1],"fim_compra","nao definiu o contexto fim_compra")
       
    def testar_comprar_segundo_nivel_sem_contexto_falha(self):
        self.brain.clearContexts()
        result = self.brain.GetMostProbableIntent("quero comprar um eletrodoméstico")
        self.assertEqual(result["intent"],None,"nao deveria achar um Intent mas achou")
        
if __name__ == '__main__':
    unittest.main()
