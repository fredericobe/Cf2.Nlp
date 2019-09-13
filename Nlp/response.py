from jsonConvert import JsonConvert

@JsonConvert.register
class Response():
    
    def __init__(self): 
        self.intentMatched = False
        self.inputSentece = ""
        self.selectedIntentName = ""
        self.accuracy = 1
        self.currentContexts = []
        self.intentResponseType = ""
        self.intentResponseValue = ""
        