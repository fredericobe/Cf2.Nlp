from jsonConvert import JsonConvert

@JsonConvert.register
class BrainEntity(object):
    def __init__(self):
        self.Name = ""
        self.Language = ""
        self.AccuracyFactor = 1

        


