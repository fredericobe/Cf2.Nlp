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
from corpusHelper import CorpusHelper

class Test_Learn_Brain(unittest.TestCase):

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
        self.memoryComplex.AddEntity(entity)
        
        intent = Intent()
        intent.Name ="pedras"
        intent.addTrainingPhrase("qual a intenção de {entity:{name:mineral}}")
        intent.addTrainingPhrase("me diga o assunto de {entity:{name:mineral}}")



        self.memoryComplex.AddIntent(intent)

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
        self.memoryComplex.AddEntity(entity)
        
        intent = Intent()
        intent.Name ="bicho"
        intent.addTrainingPhrase("qual a intenção de {entity:{name:bicho}} ")
        intent.addTrainingPhrase("me diga o assunto de {entity:{name:bicho}}")

        self.expectedCorpusBicho= {'intenç': 1, 'bicho': 2, 'dig': 1, 'assunt': 1} 

        self.memoryComplex.AddIntent(intent)


        self.memorySimple = Memory()

        intent = Intent()
        intent.Name ="amor"
        intent.addTrainingPhrase("Eu te amo")
        intent.addTrainingPhrase("Você é o amor da minha vida")

        self.memorySimple.AddIntent(intent)
        self.expectedCorpusAmor = {'amo': 1, 'é': 1, 'am': 1, 'vid': 1}

        self.memoryMedo = Memory()
        intent = Intent()
        intent.Name ="medo"
        intent.addTrainingPhrase("estou com medo")
        intent.addTrainingPhrase("tenho medo de fantasma")
        self.memoryMedo.AddIntent(intent)

        

        #self.expectedCorpusMedo = {'est': 1, 'med': 2, 'tenh': 1, 'fantasm': 1}
        self.expectedCorpusMedo = { 'med': 2, 'fantasm': 1}

    def testar_isParam(self):
        b = CorpusHelper()
        ret = b._isParam("__teste_1__")
        
        self.assertTrue(ret)
    
    def testar_isParamFalse(self):
        b = CorpusHelper()
        ret = b._isParam(" __teste_1__")
        self.assertFalse(ret)

    def testar_isParamFalse2(self):
        b = CorpusHelper()
        ret = b._isParam("asd__teste_1__")
        self.assertFalse(ret)

   

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
        self.assertEquals(self.expectedCorpusBicho[i.Corpus[0].value.stem],i.Corpus[0].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusBicho[i.Corpus[1].value],i.Corpus[1].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusBicho[i.Corpus[2].value.stem],i.Corpus[2].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusBicho[i.Corpus[3].value.stem],i.Corpus[3].strength, "O Corpus nao bateu")
        
        
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
        self.assertEquals(self.expectedCorpusPedras[i.Corpus[0].value.stem],i.Corpus[0].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusPedras[i.Corpus[1].value],i.Corpus[1].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusPedras[i.Corpus[2].value.stem],i.Corpus[2].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusPedras[i.Corpus[3].value.stem],i.Corpus[3].strength, "O Corpus nao bateu")
        

    def testar_learn_medo(self):
        word = WordProcess()
        b = Brain(word,self.memoryMedo)
        b.Learn()
        i = b.Memory.GetIntent("medo")
        self.assertEquals(len(i.Corpus),len(self.expectedCorpusMedo))
    
    def testar_learn_amor_length(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        i = b.Memory.GetIntent("amor")
        
        self.assertEquals(len(i.Corpus),4, "O Corpus nao bateu")

    def testar_learn_amor(self):
        word = WordProcess()
        b = Brain(word,self.memorySimple)
        b.Learn()
        i = b.Memory.GetIntent("amor")
        #self.assertEquals(i.Corpus,self.expectedCorpusAmor, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[0].value.stem],i.Corpus[0].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[1].value.stem],i.Corpus[1].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[2].value.stem],i.Corpus[2].strength, "O Corpus nao bateu")
        self.assertEquals(self.expectedCorpusAmor[i.Corpus[3].value.stem],i.Corpus[3].strength, "O Corpus nao bateu")
       # self.assertEquals(self.expectedCorpusAmor[i.Corpus[4].value],i.Corpus[4].strength, "O Corpus nao bateu")
        #self.assertEquals(self.expectedCorpusAmor[i.Corpus[5].value],i.Corpus[5].strength, "O Corpus nao bateu")
        

 
    

if __name__ == '__main__':
    unittest.main()