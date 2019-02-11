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
class TestBrain(unittest.TestCase):

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
        self.expectedCorpusAmor = {'amo': 1, 'voc': 1, 'é': 1, 'am': 1, 'minh': 1, 'vid': 1}


        intent = Intent()
        intent.Name ="medo"
        intent.addTrainingPhrase("estou com medo")
        intent.addTrainingPhrase("tenho medo de fantasma")
        self.memorySimple.Intents.append(intent)

        

        self.expectedCorpusMedo = {'est': 1, 'med': 2, 'tenh': 1, 'fantasm': 1}


    def testar_isParam(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        ret = b._isParam("__teste_1__")
        
        self.assertTrue(ret)
    
    def testar_isParamFalse(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        ret = b._isParam(" __teste_1__")
        self.assertFalse(ret)

    def testar_isParamFalse2(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        ret = b._isParam("asd__teste_1__")
        self.assertFalse(ret)

    def testar_getTypeNameFromParam(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        ret = b._getTypeNameFromParam("__teste_1__")
        self.assertEquals(ret,"teste")


    def testar_learn_bicho_length(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        b.Learn()
        i = b.Memory.GetIntent("bicho")
        self.assertEquals(len(i.Corpus),len(self.expectedCorpusBicho), "O Corpus nao bateu")

        
    def testar_learn_bicho(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        b.Learn()
        i = b.Memory.GetIntent("bicho")
        self.assertEquals(len(i.Corpus),len(self.expectedCorpusBicho), "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusBicho[i.Corpus[0].value],i.Corpus[0].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusBicho[i.Corpus[1].value],i.Corpus[1].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusBicho[i.Corpus[2].value],i.Corpus[2].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusBicho[i.Corpus[3].value],i.Corpus[3].strength, "O Corpus nao bateu")
        
        
    def testar_learn_bicho_length(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        b.Learn()
        i = b.Memory.GetIntent("bicho")
        self.assertEquals(len(i.Corpus),len(self.expectedCorpusBicho), "O Corpus nao bateu")
        
     
    def testar_learn_pedra(self):
        word = WordProcess()
        b = Brain(word,self.memoryComplex)
        b.Learn()
        i = b.Memory.GetIntent("pedras")
        
        self.assertEquals(len(i.Corpus),len(self.expectedCorpusPedras), "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusPedras[i.Corpus[0].value],i.Corpus[0].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusPedras[i.Corpus[1].value],i.Corpus[1].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusPedras[i.Corpus[2].value],i.Corpus[2].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusPedras[i.Corpus[3].value],i.Corpus[3].strength, "O Corpus nao bateu")
        

    def testar_learn_medo(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        i = b.Memory.GetIntent("medo")
        self.assertEquals(len(i.Corpus),len(self.expectedCorpusMedo))
    
    def testar_learn_amor_length(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        i = b.Memory.GetIntent("amor")
        
        self.assertEquals(len(i.Corpus),6, "O Corpus nao bateu")

    def testar_learn_amor(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        i = b.Memory.GetIntent("amor")
        #self.assertEquals(i.Corpus,self.expectedCorpusAmor, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[0].value],i.Corpus[0].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[1].value],i.Corpus[1].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[2].value],i.Corpus[2].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[3].value],i.Corpus[3].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[4].value],i.Corpus[4].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[5].value],i.Corpus[5].strength, "O Corpus nao bateu")
        

    def testar_score_de_intent_sucesso_medo(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        i = b.Memory.GetIntent("medo")
        result = b.CalculateIntentScore("tenho medo de aranhas",i)
        self.assertEquals(result['score'],3)

    def testar_score_de_intent_sucesso_amor(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        i = b.Memory.GetIntent("amor")
        result = b.CalculateIntentScore("eu amo aquela menina",i)
        self.assertEquals(result['score'],1)

    
    def testar_score_de_intent_falha(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        i = b.Memory.GetIntent("amor")
        result = b.CalculateIntentScore("tenho medo de aranhas",i)
        self.assertEquals(int(result['score']),0)

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
        b.AccuracyFactor=0.4
        result = b.GetMostProbableIntent("tenho amor por você")
        self.assertEquals(result['intent'].Name,"amor")

if __name__ == '__main__':
    unittest.main()