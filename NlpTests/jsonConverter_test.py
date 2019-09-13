import unittest
import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('../')
from jsonConvert import JsonConvert
from memory import Memory
from intent import Intent
from bson import BSON
from bson import ObjectId
class Test_brain_context_test(unittest.TestCase):


    def setUp(self):
        pass
       
    def testar_importar_json(self):
        #Memory Object
        x = '{\n'
        x = x +'    "Entities": [],\n'
        x = x +'    "Intents": [\n'
        x = x +'        {\n'
        x = x +'            "Completed": null,\n'
        x = x +'            "Corpus": [],\n'
        x = x +'            "InputContexts": [],\n'
        x = x +'            "Name": "Boas_Vindas",\n'
        x = x +'            "OutputContexts": [],\n'
        x = x +'            "Parameters": {},\n'
        x = x +'            "Responses": [\n'
        x = x +'                "Ol\\u00e1, vou bem e voc\\u00ea?",\n'
        x = x +'                "Estou \\u00f3timo, obrigado por perguntar!"\n'
        x = x +'            ],\n'
        x = x +'            "_trainingPhrases": [\n'
        x = x +'                {\n'
        x = x +'                    "Corpus": [],\n'
        x = x +'                    "TotalStrength": 0,\n'
        x = x +'                    "_hasEntity": null,\n'
        x = x +'                    "_originalSentence": "Ol\\u00e1, tudo bem?",\n'
        x = x +'                    "_sentence": "Ol\\u00e1, tudo bem?",\n'
        x = x +'                    "params": {}\n'
        x = x +'                },\n'
        x = x +'                {\n'
        x = x +'                    "Corpus": [],\n'
        x = x +'                    "TotalStrength": 0,\n'
        x = x +'                    "_hasEntity": null,\n'
        x = x +'                    "_originalSentence": "Oi, como vai?",\n'
        x = x +'                    "_sentence": "Oi, como vai?",\n'
        x = x +'                    "params": {}\n'
        x = x +'                },\n'
        x = x +'                {\n'
        x = x +'                    "Corpus": [],\n'
        x = x +'                    "TotalStrength": 0,\n'
        x = x +'                    "_hasEntity": null,\n'
        x = x +'                    "_originalSentence": "eae, tudo bem?",\n'
        x = x +'                    "_sentence": "eae, tudo bem?",\n'
        x = x +'                    "params": {}\n'
        x = x +'                }\n'
        x = x +'            ]\n'
        x = x +'        }\n'
        x = x +'    ],\n'
        x = x +'    "_id": {\n'
        x = x +'        "$oid": "5d2e8a5c48768aa67c80ead3"\n'
        x = x +'    }\n'
        x = x +'}'
        
        y = JsonConvert.FromJSON(x)
        self.assertIsInstance(y,tempMemory)
        self.assertEquals(str(y._id),"5d2e8a5c48768aa67c80ead3")
        self.assertEquals(y.Intents[0].Name,"Boas_Vindas")    
        
@JsonConvert.register
class tempMemory():


    def __init__(self):
        self.Intents = None
        self.Entities = None
        self._id = None




if __name__ == '__main__':
    unittest.main()


