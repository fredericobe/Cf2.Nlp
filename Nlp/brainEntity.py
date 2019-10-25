from jsonConvert import JsonConvert
import json

@JsonConvert.register
class BrainEntity(object):
    def __init__(self):
        self.Name = ""
        self.Language = ""
        self.AccuracyFactor = 1
    
    #def __dict__(self):
    #    return json.dumps(self, default=lambda o: o.__dict__, 
    #        sort_keys=True, indent=4)

        


