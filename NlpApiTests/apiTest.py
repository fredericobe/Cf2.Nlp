import unittest
import sys

sys.path.append('Nlp')
sys.path.append('/Nlp')
sys.path.append('../Nlp')
sys.path.append('NlpApi')
sys.path.append('/NlpApi')
sys.path.append('../NlpApi')
sys.path.append('../')


from brainApi import BrainItemApi
from brainApi import BrainListApi
from unittest.mock import Mock
from brainEntity import BrainEntity
from jsonConvert import JsonConvert

from werkzeug.exceptions import HTTPException

class Test_EntityApi(unittest.TestCase):
    
    def test_get_entity(self):
        self.fail("Not implemented")

    def test_post_entity(self):
        self.fail("Not implemented")
    
    def test_put_entity(self):
        self.fail("Not implemented")

    def test_delete_entity(self):
        self.fail("Not implemented")

class Test_BrainApiTest(unittest.TestCase):
  

    #def test_get_intent(self):
    #    self.fail("Not implemented")

    #def test_post_intent(self):
    #    self.fail("Not implemented")
    
    #def test_put_intent(self):
    #    self.fail("Not implemented")

    #def test_delete_intent(self):
    #    self.fail("Not implemented")

    def test_get_brain_404(self):
        rep = Mock()
        
        rep.getBrain.return_value = None

        brain = BrainItemApi(rep)
        with self.assertRaises(HTTPException) as htt_error:
            ret = brain.get(1)
            self.assertEqual(http_error.exception.code, 404)
        

    def test_get_brain(self):
        rep = Mock()
        
        item = BrainEntity()
        item.Name = "First Brain"
        item.Language = "pt-BR"
        item.AccuracyFactor = 1
      

        rep.getBrain.return_value = item

        brain = BrainItemApi(rep)
        ret = brain.get(1)
        obj = JsonConvert.FromJSON(ret)

        self.assertEqual(obj.Name, "First Brain")
        rep.getBrain.assert_called()
        rep.getBrain.assert_called_with(1)

    def test_get_brains_2(self):
        rep = Mock()
        item = BrainEntity()
        item.Name = "First Brain"
        item.Language = "pt-BR"
        item.AccuracyFactor = 1
        item2 = BrainEntity()
        item2.Name = "Second Brain"
        item2.Language = "pt-BR"
        item2.AccuracyFactor = 1

        rep.getBrains.return_value = [item,item2]
        brain = BrainListApi(rep)
        ret = brain.get()
        obj = JsonConvert.FromJSON(ret)

        self.assertEqual(2,len(obj))
        rep.getBrains.assert_called()

    def test_get_brains_1(self):
        rep = Mock()
        item = BrainEntity()
        item.Name = "First Brain"
        item.Language = "pt-BR"
        item.AccuracyFactor = 1
   

        rep.getBrains.return_value = [item]
        brain = BrainListApi(rep)
        ret = brain.get()
        obj = JsonConvert.FromJSON(ret)

        self.assertEqual(1,len(obj))
        rep.getBrains.assert_called()
    
 
    def test_post_brain(self):
        rep = Mock()

        rep.addBrain.return_value = 1
        brain = BrainListApi(rep)
        payload="{\n    \"Name\": \"My Brain\",\n    \"Language\": \"pt-BR\",\n    \"AccuracyFactor\": 1}"

        ret = brain.post(payload)
      
        self.assertEqual((1, 201),ret)
        rep.addBrain.assert_called()


    def test_put_brain(self):
        rep = Mock()

        rep.updateBrain.return_value = 1
        brain = BrainItemApi(rep)
        payload="{\n    \"Name\": \"My Brain\",\n    \"Language\": \"pt-BR\",\n    \"AccuracyFactor\": 1}"

        ret = brain.put(1,payload)
      
        self.assertEqual((1,200),ret)
        rep.updateBrain.assert_called()



    #def test_post_match(self):
    #    self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
