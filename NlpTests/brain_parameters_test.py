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
from regExpEntity import RegExpEntity

class Test_brain_parameters_test(unittest.TestCase):

    def setUp(self):
        
        word = WordProcess()
        self.memory = Memory()
        
        intent = Intent()
        intent.Name ="pedras"
        intent.addTrainingPhrase("seleção de {entity:{name:mineral}}")
        intent.addTrainingPhrase("uma {entity:{name:mineral}} é um mineral")
       
        intent.addResponse("Mineral escolhido")
        
        self.memory.AddIntent(intent)


        intent = Intent()
        intent.Name ="pedras_e_metais"
        intent.addTrainingPhrase("seleção de {entity:{name:mineral}} e {entity:{name:mineral}}")
       
        intent.addResponse("metal e pedra escolhido")
        
        self.memory.AddIntent(intent)


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
        self.memory.AddEntity(entity)

        intent = Intent()
        intent.Name ="url"
        intent.addTrainingPhrase("salva essa url {entity:{name:sysurl}}")
        intent.addTrainingPhrase("{entity:{name:sysurl}}")
       
        intent.addResponse("URL salva")
        self.memory.AddIntent(intent)

        intent = Intent()
        intent.Name ="email"
        intent.addTrainingPhrase("meu email é {entity:{name:sysemail}}")
        intent.addTrainingPhrase("{entity:{name:sysemail}}")
       
        intent.addResponse("ok email")
        self.memory.AddIntent(intent)

        entity = RegExpEntity()
        entity.Name = "sysurl"
        entity.RegExp =  "((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))" 
        self.memory.AddEntity(entity)

        entity = RegExpEntity()
        entity.Name = "sysemail"
        entity.RegExp =  "[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+" 
        self.memory.AddEntity(entity)

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
        self.assertEqual(intent.Parameters["mineral_1"].type,"mineral","type nao bateu")
        self.assertEqual(intent.Parameters["mineral_1"].resolvedValue,"metal","resolvedValue nao bateu")

        self.assertEqual(intent.Parameters["mineral_2"].name,"mineral_2","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["mineral_2"].type,"mineral","type nao bateu")
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
    
    def test_seleciona_url(self):
        result = self.brain.GetMostProbableIntent("http://www.google.com.br")
        intent = result["intent"]
        self.assertEqual(intent.Name,"url","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["sysurl_1"].name,"sysurl_1","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["sysurl_1"].actualValue,"http://www.google.com.br","actualValue nao bateu")
        self.assertEqual(intent.Parameters["sysurl_1"].resolvedValue,"http://www.google.com.br","resolvedValue nao bateu")
    
    def test_seleciona_url_com_texto(self):
        result = self.brain.GetMostProbableIntent("salve essa url http://www.google.com.br")
        intent = result["intent"]
        self.assertEqual(intent.Name,"url","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["sysurl_1"].name,"sysurl_1","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["sysurl_1"].actualValue,"http://www.google.com.br","actualValue nao bateu")
        self.assertEqual(intent.Parameters["sysurl_1"].resolvedValue,"http://www.google.com.br","resolvedValue nao bateu")

    def test_seleciona_email(self):
        result = self.brain.GetMostProbableIntent("teste@teste.com")
        intent = result["intent"]
        self.assertEqual(intent.Name,"email","Nome do Intent não bateu")
        self.assertEqual(intent.Parameters["sysemail_1"].name,"sysemail_1","nome do parametro nao bateu")
        self.assertEqual(intent.Parameters["sysemail_1"].actualValue,"teste@teste.com","actualValue nao bateu")
        self.assertEqual(intent.Parameters["sysemail_1"].resolvedValue,"teste@teste.com","resolvedValue nao bateu")

if __name__ == '__main__':
    unittest.main()
