import unittest
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
        self.assertIsNot(result.Parameters["__mineral_1__"],None,"nome não bateu")
        

    def test_escolher_um_parametro_ouro(self):
        
        result = self.brain.GetMostProbableIntent("seleção de ouro")
        intent = result["intent"]
        self.assertEqual(intent.Name,"pedras","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["__mineral_1__"].name,"__mineral_1__","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["__mineral_1__"].actualValue,"ouro","actualValue nao bateu")
        self.assertEqual(intent.Parameters["__mineral_1__"].resolvedValue,"metal","resolvedValue nao bateu")

    def test_escolher_um_parametro_pedra(self):
        
        result = self.brain.GetMostProbableIntent("seleção de pedra")
        intent = result["intent"]
        self.assertEqual(intent.Name,"pedras","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["__mineral_1__"].name,"__mineral_1__","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["__mineral_1__"].actualValue,"pedra","actualValue nao bateu")
        self.assertEqual(intent.Parameters["__mineral_1__"].resolvedValue,"pedra","resolvedValue nao bateu")

    def test_escolher_um_parametro_rocha(self):
        
        result = self.brain.GetMostProbableIntent("seleção de rocha")
        intent = result["intent"]
        self.assertEqual(intent.Name,"pedras","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["__mineral_1__"].name,"__mineral_1__","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["__mineral_1__"].actualValue,"rocha","actualValue nao bateu")
        self.assertEqual(intent.Parameters["__mineral_1__"].resolvedValue,"pedra","resolvedValue nao bateu")


if __name__ == '__main__':
    unittest.main()
