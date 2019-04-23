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
class Test_score_Brain(unittest.TestCase):

    def setUp(self):
        
        self.memoryComplex = Memory()
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
        self.memoryComplex.Entities.append(entity)
        
        intent = Intent()
        intent.Name ="pedras"
        intent.addTrainingPhrase("qual a intenção de {entity:{name:mineral}}")
        intent.addTrainingPhrase("me diga o assunto de {entity:{name:mineral}}")



        self.memoryComplex.Intents.append(intent)

        self.expectedCorpusPedras = {'intenç': 1, 'mineral': 2, 'dig': 1, 'assunt': 1}

        


        entity = Entity()
        entity.Name = "animal"
        word = WordProcess()
        sin = Synonym(word)
        sin.setPrincipal("mamifero")
        sin.addOther("homem")
        sin.addOther("boi")
        sin.addOther("cachorro")

        entity.Synonymous.append(sin)

        sin = Synonym(word)
        sin.setPrincipal("oviparo")
        sin.addOther("pato")
        sin.addOther("galinha")
        sin.addOther("passaro")

        entity.Synonymous.append(sin)
        self.memoryComplex.Entities.append(entity)
        
        intent = Intent()
        intent.Name ="bicho"
        intent.addTrainingPhrase("qual a intenção de {entity:{name:bicho}} ")
        intent.addTrainingPhrase("me diga o assunto de {entity:{name:bicho}}")

        self.expectedCorpusBicho= {'intenç': 1, 'bicho': 2, 'dig': 1, 'assunt': 1} 

        self.memoryComplex.Intents.append(intent)


        self.memorySimple = Memory()
        intent = Intent()
        intent.Name ="amor"
        intent.addTrainingPhrase("Eu te amo")
        intent.addTrainingPhrase("Você é o amor da minha vida")

        self.memorySimple.Intents.append(intent)
        self.expectedCorpusAmor = {'amo': 1, 'é': 1, 'am': 1, 'vid': 1}


        intent = Intent()
        intent.Name ="medo"
        intent.addTrainingPhrase("estou com medo")
        intent.addTrainingPhrase("tenho medo de fantasma")
        self.memorySimple.Intents.append(intent)

         
        self.expectedCorpusMedo = { 'med': 2, 'fantasm': 1}

    def testar_obterIntentMedo(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.AccuracyFactor=0.5
        b.Learn()
        result = b.GetMostProbableIntent("tenho medo de aranhas")
        self.assertEquals(result['intent'].Name,"medo")

    def testar_obterIntentPedra_1(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        b.AccuracyFactor=0.5
        b.Learn()
        result = b.GetMostProbableIntent("qual a intenção de rocha")
        self.assertEquals(result['intent'].Name,"pedras")

    def testar_obterIntentPedra_2(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        b.AccuracyFactor=0.5
        b.Learn()
        result = b.GetMostProbableIntent("qual a intenção de pedregulho")
        self.assertEquals(result['intent'].Name,"pedras")

    def testar_obterclasseAmor(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        b.AccuracyFactor=0.2
        result = b.GetMostProbableIntent("eu amo pipoca")
        self.assertEquals(result['intent'].Name,"amor")


    def testar_obterclasseAmor2(self):      
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        b.AccuracyFactor=0.3
        result = b.GetMostProbableIntent("tenho amor por você")
        self.assertEquals(result['intent'].Name,"amor")

if __name__ == '__main__':
    unittest.main()