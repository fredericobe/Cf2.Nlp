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
class Test_brain_parameters_test(unittest.TestCase):

    def setUp(self):
        
        word = WordProcess()
        self.memory = Memory()
        
        intent = Intent()
        intent.Name ="pedras"
        intent.addTrainingPhrase("seleção de {entity:{name:mineral}}")
        intent.addTrainingPhrase("uma {entity:{name:mineral}} é um mineral")
       
        intent.addResponse("Mineral escolhido")
        
        self.memory.Intents.append(intent)


        intent = Intent()
        intent.Name ="pedras_e_metais"
        intent.addTrainingPhrase("seleção de {entity:{name:mineral}} e {entity:{name:mineral}}")
       
        intent.addResponse("metal e pedra escolhido")
        
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





    def test_verificar_nome_parametro(self):
        
        result = self.memory.GetIntent("pedras")
        
        self.assertEqual(len(result.Parameters),1,"total de parametros nao bateu")
        self.assertIsNot(result.Parameters["mineral_1"],None,"nome não bateu")
        

    
    def test_escolher_dois_parametros(self):
        
        result = self.brain.GetMostProbableIntent("seleção de ouro e rocha")
        intent = result["intent"]
       
        self.assertEqual(intent.Name,"pedras_e_metais","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["mineral_1"].name,"mineral_1","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].actualValue,"ouro","actualValue nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].resolvedValue,"metal","resolvedValue nao bateu")

        self.assertEqual(intent.Parameters["mineral_2"].name,"mineral_2","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["mineral_2"].actualValue,"rocha","actualValue nao bateu")
        self.assertEqual(intent.Parameters["mineral_2"].resolvedValue,"pedra","resolvedValue nao bateu")

    def test_escolher_um_parametro_ouro(self):
        
        result = self.brain.GetMostProbableIntent("seleção de ouro")
        intent = result["intent"]
       
        self.assertEqual(intent.Name,"pedras","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["mineral_1"].name,"mineral_1","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].actualValue,"ouro","actualValue nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].resolvedValue,"metal","resolvedValue nao bateu")

    def test_escolher_um_parametro_pedra(self):
        
        result = self.brain.GetMostProbableIntent("seleção de pedra")
        intent = result["intent"]
        self.assertEqual(intent.Name,"pedras","Nome do Intent não bteu")
        self.assertEqual(intent.Parameters["mineral_1"].name,"mineral_1","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].actualValue,"pedra","actualValue nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].resolvedValue,"pedra","resolvedValue nao bateu")

    def test_escolher_um_parametro_rocha(self):
        
        result = self.brain.GetMostProbableIntent("seleção de rocha")
        intent = result["intent"]
        self.assertEqual(intent.Name,"pedras","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["mineral_1"].name,"mineral_1","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].actualValue,"rocha","actualValue nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].resolvedValue,"pedra","resolvedValue nao bateu")

    def test_escolher_um_parametro_pedra_e_metal(self):
        
        result = self.brain.GetMostProbableIntent("seleção de rocha e ouro")
        intent = result["intent"]
        self.assertEqual(intent.Name,"pedras_e_metais","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["mineral_1"].name,"mineral_1","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].actualValue,"rocha","actualValue nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].resolvedValue,"pedra","resolvedValue nao bateu")

        self.assertEqual(intent.Parameters["mineral_2"].actualValue,"ouro","actualValue nao bateu")
        self.assertEqual(intent.Parameters["mineral_2"].resolvedValue,"metal","resolvedValue nao bateu")
    
    def test_escolher_um_parametro_metal_e_pedra(self):
        
        result = self.brain.GetMostProbableIntent("seleção de ouro e rocha")
        intent = result["intent"]
        self.assertEqual(intent.Name,"pedras_e_metais","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["mineral_1"].name,"mineral_1","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].actualValue,"ouro","actualValue nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].resolvedValue,"metal","resolvedValue nao bateu")

        self.assertEqual(intent.Parameters["mineral_2"].name,"mineral_2","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["mineral_2"].actualValue,"rocha","actualValue nao bateu")
        self.assertEqual(intent.Parameters["mineral_2"].resolvedValue,"pedra","resolvedValue nao bateu")

    #def testar_getTypeNameFromParam(self):
    #    word = WordProcess()
    #    b = Brain(word,self.memory)
    #    ret = b._getTypeNameFromParam("teste_1")
    #    self.assertEquals(ret,"teste")

if __name__ == '__main__':
    unittest.main()
